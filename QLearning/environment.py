class Environment:
    def __init__(self, start_x, start_y, end_x, end_y, game_board):
        self.game_board = game_board
        self.state_row_cnt = 50
        self.action_cnt = 50
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        self.A_in_row = start_x
        self.A_in_col = start_y
        self.end_x = end_x
        self.end_y = end_y


    def getActionItems(self):
        return (self.action_cnt, self.actions)


    def getAgentPosition(self):
        return (self.A_in_row, self.A_in_col)
    

    def isDone(self, stateR, stateC):
        done = False
        if(self.game_board[stateR*50 + stateC].is_obs == True):
            done = True
        if (((stateR == self.end_x) and (stateC == self.end_y))):
            done = True
        return done


    def step(self, action):
        done = False
        victory = False
        R = 0
        prev_A_in_row = self.A_in_row
        prev_A_in_col = self.A_in_col

        if (action == 'UP'):
            self.A_in_row = max(self.A_in_row - 1, 0)
            R -= 1
        if (action == 'DOWN'):
            self.A_in_row = min(self.A_in_row + 1, self.state_row_cnt - 1)
            R -= 1
        if (action == 'LEFT'):
            self.A_in_col = max(self.A_in_col - 1, 0)
            R -= 1
        if (action == 'RIGHT'):
            self.A_in_col = min(self.A_in_col + 1, self.action_cnt - 1)
            R -= 1

        if (self.isDone(self.A_in_row, self.A_in_col) == True):
            done = True
            if ((self.A_in_row == self.end_x) and (self.A_in_col == self.end_y)):
                print('Target reached')
                victory = True
                R += 1000
            else:
                R -= 100
            
        next_state = (self.A_in_row, self.A_in_col)
        return (next_state, R, done, victory)
