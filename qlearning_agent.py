from greenhouse import GreenHouse

env = GreenHouse()

episodes = 15

for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        n_state, reward, done = env.step(action)
        score += reward
    print('Episode: {} Score:{}'.format(episode, score))

