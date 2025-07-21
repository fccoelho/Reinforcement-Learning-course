"""
Implementation of trainin  agent for Mountain Car Continuous Environment using OpenAI Gym
"""

import gymnasium as gym
from stable_baselines3 import PPO

TRAIN = True

# Create the environment
env = gym.make("MountainCarContinuous-v0", render_mode="rgb_array")

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)
if TRAIN:
    # Train the model
    print ("Training the model")
    model.learn(total_timesteps=100000)

    # Save the model
    model.save("ppo_mountain_car_continuous")

# Load the model
model = PPO.load("ppo_mountain_car_continuous")

# Evaluate the trained model
print("Evaluating the model")
obs, info = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    state, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
