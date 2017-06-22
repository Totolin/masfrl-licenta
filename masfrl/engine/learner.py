import threading
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Learner:
    def __init__(self, environment, display=False):

        self.environment = environment
        self.discount = 0.3
        # Gamma decides weather we explore or not
        self.gamma = 0.8
        self.gamma_decay = 0.99  # Exploration/exploitation tradeoff
        self.actions = self.environment.actions
        self.states = []
        self.Q = {}
        self.show_display = display
        self.prepare()

    def prepare(self):
        # Create states map based on grid
        for i in range(self.environment.x):
            for j in range(self.environment.y):
                self.states.append((i, j))

        # Create Q table based on all states and actions
        for state in self.states:
            temp = {}
            for action in self.actions:
                temp[action] = 0.1
                self.environment.set_cell_score(state, action, temp[action])
                self.Q[state] = temp

        # Set cell scores for green blocks and red blocks
        for (i, j, c, w) in self.environment.specials:
            for action in self.actions:
                self.Q[(i, j)][action] = w
                self.environment.set_cell_score((i, j), action, w)

    def import_work(self, new_Q):
        logger.info('Importing work from agent')
        for state in self.states:
            for action in self.actions:
                if state in new_Q:
                    if new_Q[state][action] != self.Q[state][action]:
                        logger.debug('Importing cell value for state %s' % str(state))
                        self.Q[state][action] = new_Q[state][action]
                        self.environment.set_cell_score(state, action, new_Q[state][action])

    def do_action(self, action):
        s = self.environment.get_player()
        r = -self.environment.score
        if action == self.actions[0]:
            self.environment.try_move(0, -1)
        elif action == self.actions[1]:
            self.environment.try_move(0, 1)
        elif action == self.actions[2]:
            self.environment.try_move(-1, 0)
        elif action == self.actions[3]:
            self.environment.try_move(1, 0)
        else:
            return
        s2 = self.environment.get_player()
        r += self.environment.score
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
        self.environment.set_cell_score(s, a, self.Q[s][a])

    def run_display(self):
        self.environment.run_display()

    def start(self):
        if self.show_display:
            t = threading.Thread(target=self.run)
            t.daemon = True
            t.start()
            self.run_display()
        else:
            self.run()

    def run(self):
        if self.show_display:
            time.sleep(1)
        alpha = 1
        t = 1
        # If its taking too long, then restart and try again
        max_run_iter = 5000
        cur_iter = 0

        while True:

            # If we ended in an loop, restart game
            cur_iter += 1
            if cur_iter > max_run_iter:
                cur_iter = 0
                self.environment.restart_game()

            # Pick the right action
            s = self.environment.get_player()
            max_act, max_val = self.max_Q(s)

            # Exploration/Exploitation tradeoff
            if np.random.rand(1) <= self.gamma:
                max_act = np.random.choice(self.actions)

            (s, a, r, s2) = self.do_action(max_act)

            # Update Q
            max_act, max_val = self.max_Q(s2)
            self.inc_Q(s, a, alpha, r + self.discount * max_val)

            # Check if the game has restarted
            t += 1.0
            if self.environment.has_restarted():
                self.environment.restart_game()
                self.gamma *= self.gamma_decay
                if self.show_display:
                    time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            alpha = pow(t, -0.1)

            # Reduce sleep time to get results faster
            if self.show_display:
                time.sleep(0.01)

