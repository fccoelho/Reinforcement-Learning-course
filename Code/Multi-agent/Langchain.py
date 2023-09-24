import tenacity
import inspect
import collections
from langchain.output_parsers import RegexParser
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI


class GymnasiumAgent:
    @classmethod
    def get_docs(cls, env):
        return env.unwrapped.__doc__

    def __init__(self, model, env):
        self.model = model
        self.env = env
        self.docs = self.get_docs(env)

        self.instructions = """
Your goal is to maximize your return, i.e. the sum of the rewards you receive.
I will give you an observation, reward, terminiation flag, truncation flag, and the return so far, formatted as:

Observation: <observation>
Reward: <reward>
Termination: <termination>
Truncation: <truncation>
Return: <sum_of_rewards>

You will respond with an action, formatted as:

Action: <action>

where you replace <action> with your actual action.
Do nothing else but return the action.
"""
        self.action_parser = RegexParser(
            regex=r"Action: (.*)", output_keys=["action"], default_output_key="action"
        )

        self.message_history = []
        self.ret = 0

    def random_action(self):
        action = self.env.action_space.sample()
        return action

    def reset(self):
        self.message_history = [
            SystemMessage(content=self.docs),
            SystemMessage(content=self.instructions),
        ]

    def observe(self, obs, rew=0, term=False, trunc=False, info=None):
        self.ret += rew

        obs_message = f"""
Observation: {obs}
Reward: {rew}
Termination: {term}
Truncation: {trunc}
Return: {self.ret}
        """
        self.message_history.append(HumanMessage(content=obs_message))
        return obs_message

    def _act(self):
        act_message = self.model(self.message_history)
        self.message_history.append(act_message)
        action = int(self.action_parser.parse(act_message.content)["action"])
        return action

    def act(self):
        try:
            for attempt in tenacity.Retrying(
                stop=tenacity.stop_after_attempt(2),
                wait=tenacity.wait_none(),  # No waiting time between retries
                retry=tenacity.retry_if_exception_type(ValueError),
                before_sleep=lambda retry_state: print(
                    f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
                ),
            ):
                with attempt:
                    action = self._act()
        except tenacity.RetryError as e:  # noqa: F841
            action = self.random_action()
        return action

class PettingZooAgent(GymnasiumAgent):
    @classmethod
    def get_docs(cls, env):
        return inspect.getmodule(env.unwrapped).__doc__

    def __init__(self, name, model, env):
        super().__init__(model, env)
        self.name = name

    def random_action(self):
        action = self.env.action_space(self.name).sample()
        return action
    
class ActionMaskAgent(PettingZooAgent):
    def __init__(self, name, model, env):
        super().__init__(name, model, env)
        self.obs_buffer = collections.deque(maxlen=1)

    def random_action(self):
        obs = self.obs_buffer[-1]
        action = self.env.action_space(self.name).sample(obs["action_mask"])
        return action

    def reset(self):
        self.message_history = [
            SystemMessage(content=self.docs),
            SystemMessage(content=self.instructions),
        ]

    def observe(self, obs, rew=0, term=False, trunc=False, info=None):
        self.obs_buffer.append(obs)
        return super().observe(obs, rew, term, trunc, info)

    def _act(self):
        valid_action_instruction = "Generate a valid action given by the indices of the `action_mask` that are not 0, according to the action formatting rules."
        self.message_history.append(HumanMessage(content=valid_action_instruction))
        return super()._act()

def main(agents, env):
    env.reset()

    for name, agent in agents.items():
        agent.reset()

    for agent_name in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        obs_message = agents[agent_name].observe(
            observation, reward, termination, truncation, info
        )
        print(obs_message)
        if termination or truncation:
            action = None
        else:
            action = agents[agent_name].act()
        print(f"Action: {action}")
        env.step(action)
    env.close()

def rock_paper_scissors():
    from pettingzoo.classic import rps_v2

    env = rps_v2.env(max_cycles=3, render_mode="human")
    agents = {
        name: PettingZooAgent(name=name, model=ChatOpenAI(temperature=1, openai_api_key=KEY), env=env)
        for name in env.possible_agents
    }
    main(agents, env)


def tic_tac_toe():
    from pettingzoo.classic import tictactoe_v3

    env = tictactoe_v3.env(render_mode="human")
    agents = {
        name: ActionMaskAgent(name=name, model=ChatOpenAI(temperature=0.2, openai_api_key=KEY), env=env)
        for name in env.possible_agents
    }
    main(agents, env)


def texas_holdem_no_limit():
    from pettingzoo.classic import texas_holdem_no_limit_v6

    env = texas_holdem_no_limit_v6.env(num_players=4, render_mode="human")
    agents = {
        name: ActionMaskAgent(name=name, model=ChatOpenAI(temperature=0.2, openai_api_key=KEY), env=env)
        for name in env.possible_agents
    }
    main(agents, env)


if __name__ == "__main__":
    KEY = "ADD you OpenAI API key here"
    rock_paper_scissors()
    tic_tac_toe()
    texas_holdem_no_limit()
