from greenhouse import GreenHouse
import matplotlib.pyplot as plt
import numpy as np
import math

class Agent():
    def __init__(self):
        self.episodes = 10000
        self.min_alpha = 0.1
        self.min_epsilon = 0.1
        self.gamma = 1.0
        self.decay_rate = 25
       
        self.rewards = np.zeros(self.episodes)
    
    def choose_action(self, env, state, epsilon, Q_table):
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q_table[state])
        
        return action

    '''
        * learning rate and exploration rate declines with episodes
        * more likely to explore in the beginning and more likely to follow the policy in the end
    '''
    def get_alpha(self, episode):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((episode + 1) / self.decay_rate)))

    def get_epsilon(self, episode):
        return max(self.min_epsilon, min(1.0, 1.0 - math.log10((episode + 1) / self.decay_rate)))

    def update_Qtable(self, Q_table, state, next_state, action, reward, alpha):
        Q_table[state][action] += alpha * (reward + self.gamma * np.max(Q_table[next_state]) - Q_table[state][action])

if __name__ == "__main__":
    env = GreenHouse()

    agent = Agent()

    Q_table = np.zeros((650, env.action_space.n))
    
    for episode in range(agent.episodes):
        state = env.reset()
    
        alpha = agent.get_alpha(episode)
        epsilon = agent.get_epsilon(episode)

        done = False

        while not done:
            action = agent.choose_action(env, state[0], epsilon, Q_table)

            """
                * set 5 round for each action to avoid the situation like current action still benefits from previous action
                * after 5 round, update the Q table's value for current action
            """
            counter = 5
            while counter:
                next_state, reward, done = env.step(action)

                agent.rewards[episode] += reward

                counter -= 1

            agent.update_Qtable(Q_table, state[0], next_state[0], action, reward, alpha)
                
            state = next_state

    print(sum(agent.rewards) / agent.episodes)

    '''
        * Plot the traning result
            - x axis -> episode range : 0 - 10000
            - y axis -> reward range  : -300 - 300
    '''

        
    plt.figure(figsize=(20, 5))
    plt.plot(range(len(agent.rewards)), agent.rewards)
    plt.title('Q Learning Training Results')
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.savefig('Q-Learning Results.png')
    plt.show()
    



