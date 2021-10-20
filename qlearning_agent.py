from greenhouse import GreenHouse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

class Agent():
    def __init__(self, env):
        self.episodes = 1000
        self.min_alpha = 0.1
        self.min_epsilon = 0.1
        self.gamma = 1.0
        self.decay_rate = 25
        '''
            * State [weight, temperature, humidity, co2_level]
              Choose the highest state[0] as the number of states
        '''
        self.state_space = env.high[0]
        self.steps = np.zeros(self.episodes)
    
    def choose_action(self, env, state, epsilon, Q_table):
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q_table[state])
        
        return action

    '''
        learnin rate and exploration rate declines with episodes
    '''
    def get_alpha(self, episode):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((episode + 1) / self.decay_rate)))

    def get_epsilon(self, episode):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((episode + 1) / self.decay_rate)))


    def update_Qtable(self, Q_table, state, next_state, action, reward, alpha):
        Q_table[state][action] += alpha * (reward + self.gamma * np.max(Q_table[next_state]) - Q_table[state][action])


if __name__ == "__main__":
    env = GreenHouse()

    agent = Agent(env)

    Q_table = np.zeros((agent.state_space, env.action_space.n))
    
    for episode in range(agent.episodes):
        state = env.reset()
    
        alpha = agent.get_alpha(episode)
        epsilon = agent.get_epsilon(episode)

        done = False

        while not done:
            agent.steps[episode] += 1

            action = agent.choose_action(env, state[0], epsilon, Q_table)

            next_state, reward, done = env.step(action)

            agent.update_Qtable(Q_table, state[0], action, reward, next_state[0], alpha)

            state = next_state

    '''
        * Plot the traning result
          x axis : episode range
          y axis : steps to reach the plant weight good for harvest
    '''
    plot = sns.lineplot(x = range(len(agent.steps)), y = agent.steps)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.savefig('TrainingResults.png', dpi=300)
    plt.show()



