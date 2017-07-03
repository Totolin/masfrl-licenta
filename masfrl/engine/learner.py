import threading
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Define usable algorithms for the Learner as static list
leaner_algs = ['qlearn', 'sarsa']


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
        self.running = True
        self.working_thread = None
        self.alpha = 1

        self.algorithm_methods = {
            "qlearn": self.qlearn,
            "sarsa": self.sarsa
        }

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
                    if new_Q[state][action] != 0.1:
                        # logger.debug('Importing cell value for state %s, action %s' % (str(state), str(action)))
                        self.Q[state][action] = new_Q[state][action]
                        self.environment.set_cell_score(state, action, new_Q[state][action])

    def import_learner(self, new_learner):
        self.environment.reposition_player(new_learner['player'])
        self.gamma = new_learner['gamma']
        self.alpha = new_learner['alpha']

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

    def start(self, algorithm):
        if algorithm not in self.algorithm_methods:
            return False

        # Select proper algorithm to run on environment
        alg = self.algorithm_methods[algorithm]

        # Run it, either with display or without
        if self.show_display:
            self.working_thread = threading.Thread(target=alg)
            self.working_thread.daemon = True
            self.working_thread.start()
            self.run_display()
        else:
            alg()

    def stop(self):
        if self.show_display:
            self.environment.stop_display()
            self.running = False
            self.working_thread.join()
        else:
            self.running = False

    def qlearn(self):
        if self.show_display:
            time.sleep(1)
        t = 1
        # If its taking too long, then restart and try again
        max_run_iter = 5000
        cur_iter = 0

        while self.running:

            # If we the maximum number of iterations, restart game
            cur_iter += 1
            if cur_iter > max_run_iter:
                cur_iter = 0
                logger.warn('Maximum iterations reached. Restarting game')
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
            self.inc_Q(s, a, self.alpha, r + self.discount * max_val)

            # Check if the game has restarted
            t += 1.0
            if self.environment.has_restarted():
                self.environment.restart_game()
                self.gamma *= self.gamma_decay
                if self.show_display:
                    time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            self.alpha = pow(t, -0.1)

            # Reduce sleep time to get results faster
            if self.show_display:
                time.sleep(0.01)

    def sarsa(self):
        if self.show_display:
            time.sleep(1)
        t = 1

        # If its taking too long, then restart and try again
        max_run_iter = 5000
        cur_iter = 0

        while self.running:

            # If we the maximum number of iterations, restart game
            cur_iter += 1
            if cur_iter > max_run_iter:
                cur_iter = 0
                logger.warn('Maximum iterations reached. Restarting game')
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
            qnext = self.Q[s2][max_act]
            self.inc_Q(s, a, self.alpha, r + self.discount * qnext)

            # Check if the game has restarted
            t += 1.0
            if self.environment.has_restarted():
                self.environment.restart_game()
                self.gamma *= self.gamma_decay
                if self.show_display:
                    time.sleep(0.01)
                t = 1.0

            # Update the learning rate
            self.alpha = pow(t, -0.1)

            # Reduce sleep time to get results faster
            if self.show_display:
                time.sleep(0.01)

    def to_string(self):
        return {
            "gamma": self.gamma,
            "alpha": self.alpha,
            "Q": self.Q,
            "player": self.environment.get_orig_player(),
            "score": self.environment.get_max_score(),
            "successful": self.environment.successful
        }
