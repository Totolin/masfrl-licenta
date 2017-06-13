__author__ = 'philippe'
import World
import threading
import time
import numpy as np


class Learner:
    def __init__(self):

        self.discount = 0.3
        # Gamma decides weather we explore or not
        self.gamma = 0.8
        self.gamma_decay = 0.99  # Exploration/exploitation tradeoff
        self.actions = World.actions
        self.states = []
        self.Q = {}

        self.prepare()

    def prepare(self):
        # Create states map based on grid
        for i in range(World.x):
            for j in range(World.y):
                self.states.append((i, j))

        # Create Q table based on all states and actions
        for state in self.states:
            temp = {}
            for action in self.actions:
                temp[action] = 0.1
                World.set_cell_score(state, action, temp[action])
                self.Q[state] = temp

        # Set cell scores for green blocks and red blocks
        for (i, j, c, w) in World.specials:
            for action in self.actions:
                self.Q[(i, j)][action] = w
                World.set_cell_score((i, j), action, w)

    def do_action(self, action):
        s = World.player
        r = -World.score
        if action == self.actions[0]:
            World.try_move(0, -1)
        elif action == self.actions[1]:
            World.try_move(0, 1)
        elif action == self.actions[2]:
            World.try_move(-1, 0)
        elif action == self.actions[3]:
            World.try_move(1, 0)
        else:
            return
        s2 = World.player
        r += World.score
        return s, action, r, s2

    def max_Q(self, s):
        val = None
        act = None
        for a, q in self.Q[s].items():
            if val is None or (q > val):
                val = q
                act = a
        return act, val

    def inc_Q(self, s, a, alpha, inc):
        self.Q[s][a] *= 1 - alpha
        self.Q[s][a] += alpha * inc
        World.set_cell_score(s, a, self.Q[s][a])

    def run(self):
        time.sleep(1)
        alpha = 1
        t = 1
        # If its taking too long, then restart and try again
        max_run_iter = 5000
        cur_iter = 0
        while True:
            cur_iter += 1
            if cur_iter > max_run_iter:
                cur_iter = 0
                World.restart_game()

            # Pick the right action
            s = World.player
            max_act, max_val = self.max_Q(s)

            # Exploration/Exploitation tradeoff
            if np.random.rand(1) <= self.gamma:
                max_act = np.random.choice(["up", "down", "left", "right"])
                # print max_act

            (s, a, r, s2) = self.do_action(max_act)

            # Update Q
            max_act, max_val = self.max_Q(s2)
            self.inc_Q(s, a, alpha, r + self.discount * max_val)

            # Check if the game has restarted
            t += 1.0
            if World.has_restarted():
                World.restart_game()
                self.gamma *= self.gamma_decay
                time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            alpha = pow(t, -0.1)

            # Reduce sleep time to get results faster
            time.sleep(0.01)


learn = Learner()
t = threading.Thread(target=learn.run)
t.daemon = True
t.start()
World.start_game()
