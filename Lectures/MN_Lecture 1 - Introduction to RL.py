import marimo as mo
import numpy as np
import matplotlib.pyplot as plt

# Introduction to Reinforcement Learning
mo.md("""
# Lecture 1 - Introduction to Reinforcement Learning

## Key Concepts
- The RL problem
- Rewards and returns
- Value functions
- Policies
""")

# RL Problem Definition
mo.md("""
## The Reinforcement Learning Problem

RL is learning what to do - how to map situations to actions - to maximize a numerical reward signal.
""")

# Example: Simple Bandit Problem
mo.md("""
### Example: Multi-Armed Bandit
""")

bandit_probs = mo.ui.slider(1, 10, value=3, label="Number of arms")
mo.md(f"""
Selected bandit with {bandit_probs.value} arms:
{bandit_probs}
""")

# Value Function Visualization
mo.md("""
## Value Functions
""")

def plot_value_function():
    states = np.arange(10)
    values = np.random.rand(10)
    fig, ax = plt.subplots()
    ax.bar(states, values)
    ax.set_title("Example Value Function")
    return fig

mo.pyplot(plot_value_function())

# Interactive Policy Example
mo.md("""
## Policy Example
""")

epsilon = mo.ui.slider(0, 1, step=0.1, value=0.1, label="Epsilon-greedy parameter")
mo.md(f"""
Current ε-greedy policy with ε={epsilon.value}:
{epsilon}
""")

# Key Takeaways
mo.md("""
## Summary
- RL involves learning through interaction
- The agent aims to maximize cumulative reward
- Value functions estimate future rewards
- Policies define behavior
""")
