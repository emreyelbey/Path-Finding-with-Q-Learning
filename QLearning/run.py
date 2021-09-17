import pygame, sys
from pygame.locals import *
import random, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import environment
import squares

pygame.init()
state = (0, 0)
lastmove = []

class Q:
    def __init__(self, gamma=0.9, alpha=0.9, epsilon=0.1, num_episodes=900, start_x=0, start_y=0, end_x=49, end_y=49, game_board=[]):
        self.game_board = game_board
        self.q_table = pd.DataFrame(0, index=pd.MultiIndex.from_product \
            ([
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
            26, 27, 28 ,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
            26, 27, 28 ,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
            ]),
            columns=['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.env = environment.Environment(self.start_x, self.start_y, self.end_x, self.end_y, self.game_board)
        self.action_count, self.actions = self.env.getActionItems()


    def reset_environment(self, start_x=0, start_y=0, end_x=49, end_y=49):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        del (self.env)
        self.env = environment.Environment(self.start_x, self.start_y, self.end_x, self.end_y, self.game_board)
        return self.env.getAgentPosition()


    def plot_results(self, steps, cost):
        f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        
        ax1.plot(np.arange(len(steps)), steps, 'b')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Steps')
        ax1.set_title('Episode via steps')
        
        ax2.plot(np.arange(len(cost)), cost, 'r')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Cost')
        ax2.set_title('Episode via cost')

        plt.tight_layout()  
        plt.show()


    qvictory = False
    def learn(self):
        steps = []
        costs = []
        victory_cnt = 0
        global lastmove
        global state
        for episode_cnt in range(self.num_episodes):
            state = self.reset_environment(self.start_x, self.start_y, self.end_x, self.end_y)
            done = self.env.isDone(state[0], state[1])
            step_count = 0
            cost = 0
            while not done:
                time.sleep(0.0000000001)
                if ((np.random.uniform() < self.epsilon) or ((self.q_table.loc[state, :] == 0).all())):
                    action = np.random.choice(self.actions)
                else:
                    action = self.q_table.loc[state,:].idxmax()
                    # action = self.q_table.loc[state, :].index[self.q_table.loc[state, :].values.argmax()]

                next_state, Reward, done, victory = self.env.step(action)

                if victory:
                    victory_cnt += 1
                    if self.epsilon > 0.05:
                        self.epsilon -= 0.005

                current_Q = self.q_table.loc[state, action]
                next_Q = self.q_table.loc[next_state, :].max()

                self.q_table.loc[state, action] += self.alpha * (Reward + self.gamma * next_Q - current_Q)
                state = next_state
                step_count += 1
                cost += Reward
                
            if (victory_cnt % 12 == 11):
                victory_cnt += 1
                lastmove.clear()
                m = 0
                state = self.reset_environment(self.start_x, self.start_y, self.end_x, self.end_y)
                done = self.env.isDone(state[0], state[1])
                while not done:
                    state = self.env.getAgentPosition()
                    action = self.q_table.loc[state,:].idxmax()
                    _, _, done, self.qvictory = self.env.step(action)
                    lastmove.append(state)
                    m += 1
                    if m > 200:
                        done = True

            steps.append(step_count)
            costs.append(cost)

            if (episode_cnt % 100 == 0):
                print('episode = {}'.format(episode_cnt))

            if self.qvictory:
                state = (self.end_x, self.end_y)
                break

        movelen = len(lastmove)
        for i in range(movelen-1):
            sira = (lastmove[i+1][0] * 50) + lastmove[i+1][1]
            self.game_board[sira].color_r = 128
            self.game_board[sira].color_g = 0
            self.game_board[sira].color_b = 0

        self.plot_results(steps, costs)


class Q_train:
    def __init__(self, start_x=0, start_y=0, end_x=49, end_y=49, game_board=[]):
        self.game_board = game_board
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        q = Q(gamma=0.9, alpha=0.9, epsilon=0.1, num_episodes=90000, start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, game_board=game_board)
        q.learn()

class Run:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.game_board = self.createGameBoard(self.start_x, self.start_y, self.end_x, self.end_y)
        state = (start_x, start_y)

    def createGameBoard(self, start_x, start_y, end_x, end_y):
        game_board = []
        for i in range(50):
            for j in range(50):
                game_board.append(squares.Squares(i, j, 255, 255, 255, False))

        for i in range(2500):
            if game_board[i].x_pos == start_x and game_board[i].y_pos == start_y:
                start_point = i
            if game_board[i].x_pos == end_x and game_board[i].y_pos == end_y:
                end_point = i

        for i in range(1100):
            rand = random.randint(0, 2499)
            while start_point == rand or end_point == rand:
                rand = random.randint(0, 2499)
            game_board[rand].color_r = 128
            game_board[rand].color_g = 128
            game_board[rand].color_b = 128
            game_board[rand].is_obs = True

        for i in range(2500):
            if game_board[i].x_pos == end_x and game_board[i].y_pos == end_y:
                game_board[i].color_r = 0
                game_board[i].color_g = 196
                game_board[i].color_b = 0
            if game_board[i].x_pos == start_x and game_board[i].y_pos == start_y:
                game_board[i].color_r = 0
                game_board[i].color_g = 0
                game_board[i].color_b = 196

        f = open("engel.txt", "w")
        for i in range(50):
            for j in range(50):
                if (game_board[i * 50 + j].is_obs):
                    f.write('({}, {}, {})\n'.format(i, j, 'K'))
                else:
                    f.write('({}, {}, {})\n'.format(i, j, 'B'))
        return game_board

    def train(self):
        trn = Q_train(self.start_x, self.start_y, self.end_x, self.end_y, self.game_board)

    def getState(self):
        global state
        return state