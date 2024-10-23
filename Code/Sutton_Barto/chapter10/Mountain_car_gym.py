import gymnasium as gym

if __name__ == "__main__":
    env = gym.make("MountainCar-v0", render_mode="rgb_array", goal_velocity=0.1)
