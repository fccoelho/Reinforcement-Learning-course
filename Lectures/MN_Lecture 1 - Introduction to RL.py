import marimo

__generated_with = "0.14.13"
app = marimo.App(
    width="medium",
    layout_file="layouts/MN_Lecture 1 - Introduction to RL.slides.json",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Introduction to Reinforcement Learning
    Reinforcement Learning can be thought of as a third paradigm of statistical learning, separated from Supervised (e.g., Regression models) and unsupervised learning(e.g. clustering).

    One of the main characteristics of Reinforcement Learning is that it consists of a goal-directed agent, which interacts with an environment. The agent can observe the state of the environment, and perform actions that change the state of the environment. The agent also receives rewards from the environment, which are used to evaluate the agent's actions. The goal of the agent is to maximize the total reward it receives from the environment. The environment is uncertain, leading the agent to try to balance exploitation (leveraging previous successful experiences) *vs* exploration(trying out new strategies), in its decisions.

    ![rl-loop](public/rl-loop.jpg)

    Whenever the agent take an action, the environment is modified as a result. Therefore, the correct choice of action must take into account indirect delayed consequences of all previous actions. Thus the environment can be thought of as a Markov Decision Process (MDP).

    ![mdp](public/600px-Markov_Decision_Process.png)

    ## Example: Tic-Tac-Toe
    ![Tic-tac-toe](tictactoe.png)

    Consider the game of Tic-Tac-Toe. Two players take turns placing their mark on a 3x3 grid. The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins the game. If the grid is full and no player has won, the game is a draw. The game of Tic-Tac-Toe can be thought of as a Markov Decision Process (MDP). The state of the environment is the current state of the grid. The actions of the agent are the possible moves that the agent can make. The reward of the agent is 1 if the agent wins, -1 if the agent loses, and 0 if the game is a draw. The goal of the agent is to learn a policy that maximizes the probability of winning the game.

    This simple game cannot be solved  properly using classical techniques, such as minimax or dynamic programming. 

    Here is how tic-tac-toe can be formulated as a Reinformcement Learning problem:
    - The agent is the player that is learning to play the game.
    - The environment is the game of tic-tac-toe.
    - The state of the environment is the current state of the grid.
    - The actions of the agent are the possible moves that the agent can make.

    First set up a table with a value for every possible state of the game and assiga a value to each state. The value of a state is the probability of winning the game if the agent is in that state. The value of a state can be estimated using the rewards received in previous games. The agent can use the value of a state to choose the best move to make in that state. If the agent is playng  X, all states with 3 Xs in a row, represent a victory and threfore are assigned a value of 1. Similarly, all states with 3 Os in a row, represent a loss and threfore are assigned a value of 0. All other states are assigned a value of 0.5, to start.

    The agent updates the values of the states by playing many games and estimating the probabilities of winning from each state.

    $$V(S_t) \leftarrow V(S_t)+\alpha\left[V(S_{t+1}-V(S_t)\right]$$

    where $\alpha$ is the learning rate, and $V(S_t)$ is the value of state $S_t$. This update rule is known as temporal-difference.

    Consider this [code](../Code/Sutton_Barto/chapter01/tic_tac_toe.py) that learns a strategy for winning Tic-Tac-Toe, using RL.
    """
    )
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %run ../Code/Sutton_Barto/chapter01/tic_tac_toe.py
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## A single state problem: the K-armed Bandit Problem
    The K-armed bandit problem is a simple example of a Reinforcement Learning problem. The agent is faced repeatedly with a choice. It can choose between K different actions, and receives a reward based on the action it chooses, the reward comes from a fixed probability distribution over the actions. The goal of the agent is to maximize the total reward it receives over time. The action chosen at time $t$ is denoted as $A_t$. The reward received is denoted as $R_t$. The expected value of an action $a$ is denoted as $q_*(a)$:

    $$q_*(a) = \mathrm{E}[R_t \mid A_t = a].$$

    The estimated value of an action $a$ at time $t$ is denoted as $Q_t(a)$. The value of an action is the expected reward given that action is selected. The value of an action is not known to the agent, and must be estimated based on the rewards received. The agent must balance exploration (trying out different actions to estimate their value) and exploitation (choosing the action with the highest estimated value). If the agent always chooses the action with the highest estimated value, we say that the agent is greedy. If the agent chooses a non-greedy action, we say that the agent is exploratory.

    ## Action-value Methods
    Action-value methods estimate the value of each action, and select the action with the highest estimated value. The simplest action-value method is the sample-average method. The estimated value of an action $a$ at time $t$ is the average of the rewards received when $a$ was selected up to time $t$:

    $$Q_t(a)=\frac{\sum_{i=1}^{t-1} R_i \cdot \mathbb{1}_{A_t=a}}{\sum_{i=1}^{t-1} \mathbb{1}_{A_t=a}}$$

    The greedy action is the action with the highest estimated value:
    $$A_t=argmax_a(Q_t(a))$$

    A simple alternative to the greedy action is the $\epsilon$-greedy action. With probability $\epsilon$, the agent chooses a random action. With probability $1-\epsilon$, the agent chooses the greedy action. The $\epsilon$-greedy action is a simple way to balance exploration and exploitation.

    In the code below we run a simulation of a 10-armed bandit that learns over 1000 decisions. This experiment is repeated 2000 times for multiple values of $\epsilon$.
    """
    )
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %run ../Code/Sutton_Barto/chapter02/ten_armed_testbed.py
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    To efficiently implement action-value methods, we can use the incremental update rule, to estimate the Average reward at step $n$
    $$Q_{n+1}=Q_n + \frac{1}{n}\left[R_n - Q_n \right],$$

    where $R_n$ is the reward at step $n$.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Nonstationary Reward Problems
    In the previous example, the reward distribution was stationary. The expected reward of each action did not change over time. In the nonstationary case, the expected reward of each action changes over time. Let $\alpha$ be a constant step size.

    \begin{align}
    Q_{n+1} &= Q_n + \alpha \left[R_n - Q_n \right] \\
    &= \alpha R_n + (1-\alpha) Q_n \\
    &= \alpha R_n + (1-\alpha) \left[ \alpha R_{n-1} + (1-\alpha) Q_{n-1} \right] \\
    &= \alpha R_n + (1-\alpha) \alpha R_{n-1} + (1-\alpha)^2 Q_{n-1} \\
    &= \dots\\
    &= (1-\alpha)^n Q_1 + \sum_{i=1}^n \alpha (1-\alpha)^{n-i} R_i
    \end{align}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Upper-Confidence-Bound Action Selection
    The $\epsilon$-greedy action selection method is simple, but it does not take into account the uncertainty in the estimated value of each action. The Upper-Confidence-Bound (UCB) action selection method does. It chooses the action with the highest upper confidence bound. The upper confidence bound of an action $a$ at time $t$ is defined as:
    \begin{align}
    A_t=argmax_a\left[Q_t(a) +c \sqrt{\frac{ln\, t}{N_t(a)}}\right]
    \end{align}

    where $ln\, t$ is the natural logarithm of $t$ and $N_t(a)$ is the number of times action $a$ was selected up to time $t$. The constant $c > 0$ controls the degree of exploration. The UCB action selection method is more complex than the $\epsilon$-greedy method, but it is more efficient in the long run.

    There are other action selection methods that have been proposed for this problem. Refer to the  Chapter 2 of the Sutton & Barto book for more details.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Conclusion
    So far we have explored simple approaches to the K-armed bandit problem. In the next lecture we will explore more complex explicitly including the value of the information state of the system.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
