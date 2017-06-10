import threading
import time
import numpy as np


class QLearn:
    def __init__(self, world, actions):
        self.world = world
        self.discount = 0.3
        self.gamma = 0.8  # Initial probability
        self.gamma_decay = 0.99  # Exploration/exploitation tradeoff
        self.actions = actions
        self.states = []
        self.Q = {}

        self.prepare()

    def prepare(self):
        for i in range(self.world.x):
            for j in range(self.world.y):
                self.states.append((i, j))

        for state in self.states:
            temp = {}
            for action in self.actions:
                temp[action] = 0.1
                self.world.set_cell_score(state, action, temp[action])
            self.Q[state] = temp

        for (i, j, c, w) in self.world.specials:
            for action in self.actions:
                self.Q[(i, j)][action] = w
                self.world.set_cell_score((i, j), action, w)

    def do_action(self, action):
        s = self.world.player
        r = -self.world.score
        if action == self.actions[0]:
            self.world.try_move(0, -1)
        elif action == self.actions[1]:
            self.world.try_move(0, 1)
        elif action == self.actions[2]:
            self.world.try_move(-1, 0)
        elif action == self.actions[3]:
            self.world.try_move(1, 0)
        else:
            return
        s2 = self.world.player
        r += self.world.score
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
        self.world.set_cell_score(s, a, self.Q[s][a])

    def run(self):
        alpha = 1
        t = 1
        # If its taking too long, then restart and try again
        max_run_iter = 5000
        cur_iter = 0
        while True:
            cur_iter += 1
            if cur_iter > max_run_iter:
                cur_iter = 0
                self.world.restart_game()

            # Pick the right action
            s = self.world.player
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
            if self.world.has_restarted():
                self.world.restart_game()
                self.gamma *= self.gamma_decay
                time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            alpha = pow(t, -0.1)
