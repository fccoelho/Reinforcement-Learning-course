#!/usr/bin/env python3
import gym
import ptan
import ptan.ignite as ptan_ignite
from datetime import datetime, timedelta
import argparse
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from ignite.engine import Engine
from ignite.metrics import RunningAverage
from ignite.contrib.handlers import tensorboard_logger as tb_logger

import lib.dqn_extra
from lib import dqn_model, common

NAME = "07_distrib"


SAVE_STATES_IMG = True
SAVE_TRANSITIONS_IMG = True

if SAVE_STATES_IMG or SAVE_TRANSITIONS_IMG:
    import matplotlib as mpl
    mpl.use("Agg")
    import matplotlib.pylab as plt

Vmax = 10
Vmin = -10
N_ATOMS = 51
DELTA_Z = (Vmax - Vmin) / (N_ATOMS - 1)

STATES_TO_EVALUATE = 1000
EVAL_EVERY_FRAME = 100


class DistributionalDQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(DistributionalDQN, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        conv_out_size = self._get_conv_out(input_shape)
        self.fc = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions * N_ATOMS)
        )

        self.register_buffer("supports", torch.arange(Vmin, Vmax+DELTA_Z, DELTA_Z))
        self.softmax = nn.Softmax(dim=1)

    def _get_conv_out(self, shape):
        o = self.conv(torch.zeros(1, *shape))
        return int(np.prod(o.size()))

    def forward(self, x):
        batch_size = x.size()[0]
        fx = x.float() / 256
        conv_out = self.conv(fx).view(batch_size, -1)
        fc_out = self.fc(conv_out)
        return fc_out.view(batch_size, -1, N_ATOMS)

    def both(self, x):
        cat_out = self(x)
        probs = self.apply_softmax(cat_out)
        weights = probs * self.supports
        res = weights.sum(dim=2)
        return cat_out, res

    def qvals(self, x):
        return self.both(x)[1]

    def apply_softmax(self, t):
        return self.softmax(t.view(-1, N_ATOMS)).view(t.size())


def calc_values_of_states(states, net, device="cpu"):
    mean_vals = []
    for batch in np.array_split(states, 64):
        states_v = torch.tensor(batch).to(device)
        action_values_v = net.qvals(states_v)
        best_action_values_v = action_values_v.max(1)[0]
        mean_vals.append(best_action_values_v.mean().item())
    return np.mean(mean_vals)


def save_state_images(frame_idx, states, net, device="cpu", max_states=200):
    ofs = 0
    p = np.arange(Vmin, Vmax + DELTA_Z, DELTA_Z)
    for batch in np.array_split(states, 64):
        states_v = torch.tensor(batch).to(device)
        action_prob = net.apply_softmax(net(states_v)).data.cpu().numpy()
        batch_size, num_actions, _ = action_prob.shape
        for batch_idx in range(batch_size):
            plt.clf()
            for action_idx in range(num_actions):
                plt.subplot(num_actions, 1, action_idx+1)
                plt.bar(p, action_prob[batch_idx, action_idx], width=0.5)
            plt.savefig("states/%05d_%08d.png" % (ofs + batch_idx, frame_idx))
        ofs += batch_size
        if ofs >= max_states:
            break


def save_transition_images(batch_size, predicted, projected, next_distr, dones, rewards, save_prefix):
    for batch_idx in range(batch_size):
        is_done = dones[batch_idx]
        reward = rewards[batch_idx]
        plt.clf()
        p = np.arange(Vmin, Vmax + DELTA_Z, DELTA_Z)
        plt.subplot(3, 1, 1)
        plt.bar(p, predicted[batch_idx], width=0.5)
        plt.title("Predicted")
        plt.subplot(3, 1, 2)
        plt.bar(p, projected[batch_idx], width=0.5)
        plt.title("Projected")
        plt.subplot(3, 1, 3)
        plt.bar(p, next_distr[batch_idx], width=0.5)
        plt.title("Next state")
        suffix = ""
        if reward != 0.0:
            suffix = suffix + "_%.0f" % reward
        if is_done:
            suffix = suffix + "_done"
        plt.savefig("%s_%02d%s.png" % (save_prefix, batch_idx, suffix))


def calc_loss(batch, net, tgt_net, gamma, device="cpu", save_prefix=None):
    states, actions, rewards, dones, next_states = common.unpack_batch(batch)
    batch_size = len(batch)

    states_v = torch.tensor(states).to(device)
    actions_v = torch.tensor(actions).to(device)
    next_states_v = torch.tensor(next_states).to(device)

    # next state distribution
    next_distr_v, next_qvals_v = tgt_net.both(next_states_v)
    next_actions = next_qvals_v.max(1)[1].data.cpu().numpy()
    next_distr = tgt_net.apply_softmax(next_distr_v).data.cpu().numpy()

    next_best_distr = next_distr[range(batch_size), next_actions]
    dones = dones.astype(np.bool)

    # project our distribution using Bellman update
    proj_distr = lib.dqn_extra.distr_projection(next_best_distr, rewards, dones, Vmin, Vmax, N_ATOMS, gamma)

    # calculate net output
    distr_v = net(states_v)
    state_action_values = distr_v[range(batch_size), actions_v.data]
    state_log_sm_v = F.log_softmax(state_action_values, dim=1)
    proj_distr_v = torch.tensor(proj_distr).to(device)

    if save_prefix is not None:
        pred = F.softmax(state_action_values, dim=1).data.cpu().numpy()
        save_transition_images(batch_size, pred, proj_distr, next_best_distr, dones, rewards, save_prefix)

    loss_v = -state_log_sm_v * proj_distr_v
    return loss_v.sum(dim=1).mean()


if __name__ == "__main__":
    random.seed(common.SEED)
    torch.manual_seed(common.SEED)
    params = common.HYPERPARAMS['pong']
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", default=False, action="store_true", help="Enable cuda")
    args = parser.parse_args()
    device = torch.device("cuda" if args.cuda else "cpu")

    env = gym.make(params.env_name)
    env = ptan.common.wrappers.wrap_dqn(env)
    env.seed(common.SEED)

    net = DistributionalDQN(env.observation_space.shape, env.action_space.n).to(device)

    tgt_net = ptan.agent.TargetNet(net)
    selector = ptan.actions.EpsilonGreedyActionSelector(epsilon=params.epsilon_start)
    epsilon_tracker = common.EpsilonTracker(selector, params)
    agent = ptan.agent.DQNAgent(lambda x: net.qvals(x), selector, device=device)

    exp_source = ptan.experience.ExperienceSourceFirstLast(
        env, agent, gamma=params.gamma)
    buffer = ptan.experience.ExperienceReplayBuffer(
        exp_source, buffer_size=params.replay_size)
    optimizer = optim.Adam(net.parameters(), lr=params.learning_rate)

    def process_batch(engine, batch):
        save_prefix = None
        prev_save = getattr(engine.state, "prev_save", 0)
        if SAVE_TRANSITIONS_IMG:
            interesting = any(map(lambda s: s.last_state is None or s.reward != 0.0, batch))
            if interesting and engine.state.iteration // 30000 > prev_save:
                save_prefix = "images/img_%08d" % engine.state.iteration
                engine.state.prev_save = engine.state.iteration // 30000

        optimizer.zero_grad()
        loss_v = calc_loss(batch, net, tgt_net.target_model, gamma=params.gamma,
                           device=device, save_prefix=save_prefix)
        loss_v.backward()
        optimizer.step()
        epsilon_tracker.frame(engine.state.iteration)
        if engine.state.iteration % params.target_net_sync == 0:
            tgt_net.sync()
        eval_states = getattr(engine.state, "eval_states", None)
        if eval_states is None:
            eval_states = buffer.sample(STATES_TO_EVALUATE)
            eval_states = [np.array(transition.state, copy=False) for transition in eval_states]
            engine.state.eval_states = np.array(eval_states, copy=False)

        if engine.state.iteration % EVAL_EVERY_FRAME == 0:
            engine.state.metrics["values"] = calc_values_of_states(eval_states, net, device=device)

        if SAVE_STATES_IMG and engine.state.iteration % 10000 == 0:
            save_state_images(engine.state.iteration, eval_states, net, device=device)

        return {
            "loss": loss_v.item(),
            "epsilon": selector.epsilon,
        }

    engine = Engine(process_batch)
    ptan_ignite.EndOfEpisodeHandler(exp_source, bound_avg_reward=params.stop_reward).attach(engine)
    ptan_ignite.EpisodeFPSHandler().attach(engine)

    @engine.on(ptan_ignite.EpisodeEvents.EPISODE_COMPLETED)
    def episode_completed(trainer: Engine):
        print("Episode %d: reward=%s, steps=%s, speed=%.3f frames/s, elapsed=%s" % (
            trainer.state.episode, trainer.state.episode_reward,
            trainer.state.episode_steps, trainer.state.metrics.get('avg_fps', 0),
            timedelta(seconds=trainer.state.metrics.get('time_passed', 0))))

    @engine.on(ptan_ignite.EpisodeEvents.BOUND_REWARD_REACHED)
    def game_solved(trainer: Engine):
        print("Game solved in %s, after %d episodes and %d iterations!" % (
            timedelta(seconds=trainer.state.metrics['time_passed']),
            trainer.state.episode, trainer.state.iteration))
        trainer.should_terminate = True

    logdir = f"runs/{datetime.now().isoformat(timespec='minutes')}-{params.run_name}-{NAME}"
    tb = tb_logger.TensorboardLogger(log_dir=logdir)
    RunningAverage(output_transform=lambda v: v['loss']).attach(engine, "avg_loss")

    episode_handler = tb_logger.OutputHandler(tag="episodes", metric_names=['reward', 'steps', 'avg_reward'])
    tb.attach(engine, log_handler=episode_handler, event_name=ptan_ignite.EpisodeEvents.EPISODE_COMPLETED)

    # write to tensorboard every 100 iterations
    ptan_ignite.PeriodicEvents().attach(engine)
    handler = tb_logger.OutputHandler(tag="train", metric_names=['avg_loss', 'avg_fps', "values"],
                                      output_transform=lambda a: a)
    tb.attach(engine, log_handler=handler, event_name=ptan_ignite.PeriodEvents.ITERS_100_COMPLETED)

    engine.run(common.batch_generator(buffer, params.replay_initial, params.batch_size))
