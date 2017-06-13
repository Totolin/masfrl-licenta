import numpy as np
from copy import copy, deepcopy


class Environment:
    def __init__(self):

        self.x = 25
        self.y = 25
        self.actions = ["up", "down", "left", "right"]
        self.specials = []
        self.player = None
        self.score = 1
        self.orig_player = None
        self.restart = False

        # New data
        self.red_blocks = 3
        self.green_blocks = 2
        self.walk_reward = -0.04
        self.map_grid = []
        self.walls = []

        self.initialize()

    def initialize(self):
        print('Initializing environment')
        for i in range(self.x):
            map_row = []
            for j in range(self.y):
                map_row.append(0)
            self.map_grid.append(map_row)

        for i in range(1, self.x - 1):
            for j in range(1, self.y - 1):
                self.map_grid[i][j] = np.random.choice([0, 1], p=[0.38, 0.62])

        # Perform cellular automata to generate a random grid layout
        iter_max = 7

        for iter_t in range(iter_max):
            new_map_grid = deepcopy(self.map_grid)
            for i in range(1, self.x - 1):
                for j in range(1, self.y - 1):
                    neighbour_score = 0
                    for i1 in range(-1, 2):
                        for j1 in range(-1, 2):
                            if (i1 != 0 or j1 != 0) and self.map_grid[i + i1][j + j1] == 1:
                                neighbour_score += 1
                    # print neighbour_score
                    if neighbour_score > 4:
                        new_map_grid[i][j] = 1
                    else:
                        new_map_grid[i][j] = 0
            self.map_grid = deepcopy(new_map_grid)

        for i in range(0, self.x):
            for j in range(0, self.y):
                if self.map_grid[i][j] == 1:
                    self.walls.append((i, j))

        self.player = (np.random.randint(self.x), np.random.randint(self.y))
        while self.map_grid[self.player[0]][self.player[1]] == 1:
            self.player = (np.random.randint(self.x), np.random.randint(self.y))

        self.orig_player = deepcopy(self.player)

        for i in range(self.red_blocks):
            gen_pos = (np.random.randint(self.x), np.random.randint(self.y))
            while self.map_grid[gen_pos[0]][gen_pos[1]] == 1:
                gen_pos = (np.random.randint(self.x), np.random.randint(self.y))
                self.specials.append((gen_pos[0], gen_pos[1], "red", -1))
        for i in range(self.green_blocks):
            gen_pos = (np.random.randint(self.x), np.random.randint(self.y))
            while self.map_grid[gen_pos[0]][gen_pos[1]] == 1:
                gen_pos = (np.random.randint(self.x), np.random.randint(self.y))
                self.specials.append((gen_pos[0], gen_pos[1], "green", 1))

    def get_player(self):
        return self.player

    def restart_game(self):
        self.player = deepcopy(self.orig_player)
        self.score = 1
        self.restart = False

    def has_restarted(self):
        return self.restart

    def try_move(self, dx, dy):
        if self.restart:
            self.restart_game()
        new_x = self.player[0] + dx
        new_y = self.player[1] + dy
        self.score += self.walk_reward
        # If the new position fits the requirements
        if (new_x >= 0) and (new_x < self.x) and (new_y >= 0) and (new_y < self.y) and not (
            (new_x, new_y) in self.walls):
            self.player = (new_x, new_y)
        for (i, j, c, w) in self.specials:
            if new_x == i and new_y == j:
                self.score -= self.walk_reward
                self.score += w
                if self.score > 0:
                    print("Success! score: ", self.score)
                else:
                    print("Fail! score: ", self.score)
                self.restart = True
                return
                # print "score: ", score
