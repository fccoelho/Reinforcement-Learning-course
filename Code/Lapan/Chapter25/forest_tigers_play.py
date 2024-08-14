#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "MAgent/python"))
import magent

import argparse
import torch
import numpy as np
from lib import model, data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True,
                        help="Model file to load")
    parser.add_argument("--map-size", type=int, default=64,
                        help="Size of the map, default=64")
    parser.add_argument("--render", default="render",
                        help="Directory to store renders, default=render")
    parser.add_argument("--walls-density", type=float, default=0.04,
                        help="Density of walls, default=0.04")
    parser.add_argument("--tigers", type=int, default=10,
                        help="Count of tigers, default=10")
    parser.add_argument("--deers", type=int, default=50,
                        help="Count of deers, default=50")
    parser.add_argument("--mode", default='forest', choices=['forest', 'double_attack'],
                        help="GridWorld mode, could be 'forest' or 'double_attack', default='forest'")

    args = parser.parse_args()

    if args.mode == 'forest':
        config = data.config_forest(args.map_size)
    elif args.mode == 'double_attack':
        config = data.config_double_attack(args.map_size)
    else:
        config = None

    env = magent.GridWorld(config, map_size=args.map_size)
    env.set_render_dir(args.render)
    deer_handle, tiger_handle = env.get_handles()

    env.reset()
    env.add_walls(method="random", n=args.map_size *
                                     args.map_size *
                                     args.walls_density)
    env.add_agents(deer_handle, method="random", n=args.deers)
    env.add_agents(tiger_handle, method="random", n=args.tigers)

    v = env.get_view_space(tiger_handle)
    v = (v[-1], ) + v[:2]
    net = model.DQNModel(v, env.get_feature_space(
        tiger_handle), env.get_action_space(tiger_handle)[0])
    net.load_state_dict(torch.load(args.model))
    print(net)
    total_reward = 0.0

    while True:
        view_obs, feats_obs = env.get_observation(tiger_handle)
        view_obs = np.array(view_obs)
        feats_obs = np.array(feats_obs)
        view_obs = np.moveaxis(view_obs, 3, 1)
        view_t = torch.tensor(view_obs, dtype=torch.float32)
        feats_t = torch.tensor(feats_obs, dtype=torch.float32)
        qvals = net((view_t, feats_t))
        actions = torch.max(qvals, dim=1)[1].cpu().numpy()
        actions = actions.astype(np.int32)
        env.set_action(tiger_handle, actions)
        done = env.step()
        if done:
            break
        env.render()
        env.clear_dead()
        total_reward += env.get_reward(tiger_handle).sum()

    print("Average reward: %.3f" % (total_reward / args.tigers))
