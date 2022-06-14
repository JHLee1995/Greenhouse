from greenhouse import GreenHouse
import matplotlib.pyplot as plt
import numpy as np

env = GreenHouse()
rewards = np.zeros(10000)

for episode in range(10000):
    state = env.reset()
    done = False
    #score = 0

    while not done:
        action = env.action_space.sample()
        next_state, reward, done = env.step(action)
        rewards[episode] += reward
        #score += reward
    #print('Episode:{} Score:{}'.format(episide, score))
    
print(sum(rewards) / 10000)
    
plt.figure(figsize=(20, 5))
plt.plot(range(len(rewards)), rewards)
plt.title('Non-RL Random Results')
plt.xlabel('Episodes')
plt.ylabel('Rewards')
plt.savefig('Non-RL Results.png')
plt.show()



