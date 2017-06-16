import logging
from copy import copy, deepcopy
from masfrl.engine.display import Display

# Use module logger
logger = logging.getLogger(__name__)


class Environment:
    def __init__(self, x, y, player, actions, specials, walls, walk_reward, initial_score):

        self.x = x
        self.y = y
        self.orig_player = player
        self.player = deepcopy(self.orig_player)
        self.specials = specials
        self.walls = walls
        self.walk_reward = walk_reward
        self.score = initial_score
        self.reset_score = initial_score
        self.restart = False
        self.actions = actions

        # Display
        self.display = Display(
            self.actions,
            self.get_player(),
            self.x,
            self.y,
            self.specials,
            self.walls
        )

    def get_player(self):
        return self.player

    def set_cell_score(self, state, action, val):
        self.display.set_cell_score(state, action, val)

    def restart_game(self):
        self.player = deepcopy(self.orig_player)
        self.score = self.reset_score
        self.restart = False
        self.display.restart_game(self.player)

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
            self.display.update_player(new_x, new_y)
            self.player = (new_x, new_y)
        for (i, j, c, w) in self.specials:
            if new_x == i and new_y == j:
                logger.debug('Color: %s, Gained Score: %s, Current score: %s' % (c, w, self.score))
                self.score -= self.walk_reward
                self.score += w
                if self.score > 0:
                    logger.info("Obtained a positive score : %s" % str(self.score))
                else:
                    logger.info("Obtained a negative score : %s" % str(self.score))
                self.restart = True
                return
                # print "score: ", score

    def run_display(self):
        self.display.start_game()



