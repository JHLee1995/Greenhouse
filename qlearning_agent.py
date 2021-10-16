from greenhouse import GreenHouse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

class Agent():
    def __init__(self):
        self.env = GreenHouse()
        self.episodes = 300
        self.min_learning_rate = 0.1
        self.min_epsilon = 0.1
        self.discount_factor = 1.0
        self.decay_rate = 25

        self.steps = np.zeros(self.episodes)
    
    def choose_action(self, state, epsilon, Q_table):
        if np.random.random() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = np.argmax(Q_table[state])
        
        return action

    def get_learning_rate(self, episode):
        return max(self.min_learning_rate, min(1.0, 1.0 - math.log10((episode + 1) / self.decay_rate)))

    def get_epsilon(self, episode):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((episode + 1) / self.decay_rate)))

    def update_Qtable(self, Q_table, state, next_state, action, reward, learning_rate):
        Q_table[state][action] += learning_rate * (reward + self.discount_factor * np.max(Q_table[next_state]) - Q_table[state][action])


if __name__ == "__main__":
    agent = Agent()

    Q_table = np.zeros((100, agent.env.action_space.n))
    
    for episode in range(agent.episodes):
            state = agent.env.reset()
        
            learning_rate = agent.get_learning_rate(episode)
            epsilon = agent.get_epsilon(episode)

            done = False

            while not done:
                agent.steps[episode] += 1

                action = agent.choose_action(state[0], epsilon, Q_table)

                next_state, reward, done = agent.env.step(action)

                agent.update_Qtable(Q_table, state[0], action, reward, next_state[0], learning_rate)

                state = next_state

    # Plot the traning result
    # x axis : episode range
    # y axis : steps to reach the plant weight good for harvest
    plot = sns.lineplot(x = range(len(agent.steps)), y = agent.steps)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.show()



