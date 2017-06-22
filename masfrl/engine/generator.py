import numpy as np
import logging
from copy import copy, deepcopy
from masfrl.engine.world import Environment

# Use module logger
logger = logging.getLogger(__name__)


def generate_qlearn():
    # Set environment size
    x = 40
    y = 40

    # Set actions the agent can use
    actions = ["up", "down", "left", "right"]

    # Specials are good/bad blocks (they will be generated)
    specials = []

    # Score is calculated once the agent is travelling
    score = 1

    # Number of special blocks to generate
    red_blocks = 3
    green_blocks = 2

    # Travelling father decreases score
    walk_reward = -0.04

    # Keep the map grid and walls in variables
    map_grid = []
    walls = []

    logger.info('Initializing Q-Learning Environment')
    for i in range(x):
        map_row = []
        for j in range(y):
            map_row.append(0)
        map_grid.append(map_row)

    for i in range(1, x - 1):
        for j in range(1, y - 1):
            map_grid[i][j] = np.random.choice([0, 1], p=[0.38, 0.62])

    # Perform cellular automata to generate a random grid layout
    iter_max = 7
    for iter_t in range(iter_max):
        new_map_grid = deepcopy(map_grid)
        for i in range(1, x - 1):
            for j in range(1, y - 1):
                neighbour_score = 0
                for i1 in range(-1, 2):
                    for j1 in range(-1, 2):
                        if (i1 != 0 or j1 != 0) and map_grid[i + i1][j + j1] == 1:
                            neighbour_score += 1
                if neighbour_score > 4:
                    new_map_grid[i][j] = 1
                else:
                    new_map_grid[i][j] = 0
        map_grid = deepcopy(new_map_grid)

    # Copy walls from map grid to a separate variable
    for i in range(0, x):
        for j in range(0, y):
            if map_grid[i][j] == 1:
                walls.append((i, j))

    # Initialize player
    player = (np.random.randint(x), np.random.randint(y))
    while map_grid[player[0]][player[1]] == 1:
        player = (np.random.randint(x), np.random.randint(y))

    # Generate specials blocks
    for i in range(red_blocks):
        gen_pos = (np.random.randint(x), np.random.randint(y))
        while map_grid[gen_pos[0]][gen_pos[1]] == 1:
            gen_pos = (np.random.randint(x), np.random.randint(y))
        specials.append((gen_pos[0], gen_pos[1], "red", -1))
    for i in range(green_blocks):
        gen_pos = (np.random.randint(x), np.random.randint(y))
        while map_grid[gen_pos[0]][gen_pos[1]] == 1:
            gen_pos = (np.random.randint(x), np.random.randint(y))
        specials.append((gen_pos[0], gen_pos[1], "green", 1))

    return Environment(x, y, player, actions, specials, walls, walk_reward, score)
