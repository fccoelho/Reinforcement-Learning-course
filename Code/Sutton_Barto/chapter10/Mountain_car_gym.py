import gymnasium as gym
import numpy as np
from tqdm import tqdm

class ValueFunction:
    def __init__(self, alpha, num_of_tilings):
        self.alpha = alpha
        self.num_of_tilings = num_of_tilings
        self.weights = np.zeros((num_of_tilings, env.observation_space.shape[0] + 1, env.action_space.n))
        self.position_scale = self.num_of_tilings / (env.observation_space.high[0] - env.observation_space.low[0])
        self.velocity_scale = self.num_of_tilings / (env.observation_space.high[1] - env.observation_space.low[1])

    def get_tile_indices(self, state):
        position, velocity = state
        position_scaled = int(position * self.position_scale)
        velocity_scaled = int(velocity * self.velocity_scale)
        return position_scaled, velocity_scaled

    def value(self, state, action):
        position_scaled, velocity_scaled = self.get_tile_indices(state)
        velocity_scaled = min(2, abs(velocity_scaled))
        return np.sum(self.weights[position_scaled, velocity_scaled, action])

    def update(self, state, action, target):
        position_scaled, velocity_scaled = self.get_tile_indices(state)
        velocity_scaled = min(2, abs(velocity_scaled))
        self.weights[position_scaled, velocity_scaled, action] += self.alpha * (target - self.value(state, action))

def epsilon_greedy_policy(state, value_function, epsilon):
    if np.random.rand() < epsilon:
        return env.action_space.sample()
    else:
        values = [value_function.value(state, action) for action in range(env.action_space.n)]
        return np.argmax(values)

def semi_gradient_n_step_sarsa(env, value_function, n, alpha, gamma, epsilon, episodes):
    for episode in range(episodes):
        print("Episode: ", episode)
        state = env.reset()[0]
        action = epsilon_greedy_policy(state, value_function, epsilon)
        states = [state]
        actions = [action]
        rewards = [0]
        T = 100000#float('inf')
        t = 0
        while True:
            # print(t)
            if t < T:
                next_state, reward, done, _, _ = env.step(action)
                rewards.append(reward)
                if done:
                    T = t + 1
                else:
                    next_action = epsilon_greedy_policy(next_state, value_function, epsilon)
                    states.append(next_state)
                    actions.append(next_action)
            tau = t - n + 1
            if tau >= 0:
                G = sum([gamma ** (i - tau - 1) * rewards[i] for i in range(tau + 1, min(tau + n, T) + 1)])
                if tau + n < T:
                    G += gamma ** n * value_function.value(states[tau + n], actions[tau + n])
                value_function.update(states[tau], actions[tau], G)
            if tau == T - 1:
                break
            t += 1
            state = next_state
            action = next_action
            # env.render()

# Evaluate the performance
def evaluate_policy(env, value_function, episodes=10):
    returns = []
    for _ in range(episodes):
        state = env.reset()[0]
        total_reward = 0
        done = False
        while not done:
            action = epsilon_greedy_policy(state, value_function, 0)  # Greedy policy
            state, reward, done, _, _ = env.step(action)
            total_reward += reward
            # env.render()
        returns.append(total_reward)
    return np.mean(returns)

if __name__ == "__main__":
    num_of_tilings = 8
    alpha = 0.1 / num_of_tilings
    gamma = 1.0
    epsilon = 0.1
    n = 4
    episodes = 50
    env = gym.make("MountainCar-v0", render_mode="human", goal_velocity=0.1)
    env.reset(seed=123, options={"x_init": np.pi / 2, "y_init": 0.5})

    value_function = ValueFunction(alpha, num_of_tilings)
    semi_gradient_n_step_sarsa(env,value_function, n, alpha, gamma, epsilon, episodes)

    print("Average return over 10 evaluation episodes:", evaluate_policy(env, value_function))