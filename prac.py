import gym
env = gym.make("MountainCar-v0")
env.reset()

done = False

while True:
    action = 2
    new_state, reward, done, _ = env.step(action)
    env.render()

env.close()