import logging
from Tkinter import *
master = Tk()

# Use module logger
logger = logging.getLogger(__name__)


class Display:
    def __init__(self, actions, player, x, y, specials, walls):
        self.triangle_size = 0.1
        self.cell_score_min = -0.2
        self.cell_score_max = 0.2
        self.Width = 20
        self.board = Canvas(master, width=x * self.Width, height=y * self.Width)
        self.cell_scores = {}
        self.actions = actions

        self.render_grid(x, y, specials, walls)

        self.me = self.board.create_rectangle(
            player[0] * self.Width + self.Width * 2 / 10,
            player[1] * self.Width + self.Width * 2 / 10,
            player[0] * self.Width + self.Width * 8 / 10,
            player[1] * self.Width + self.Width * 8 / 10,
            fill="orange", width=1, tag="me"
        )

        self.board.grid(row=0, column=0)

    def create_triangle(self, i, j, action):
        if action == self.actions[0]:
            return self.board.create_polygon((i + 0.5 - self.triangle_size) * self.Width,
                                             (j + self.triangle_size) * self.Width,
                                             (i + 0.5 + self.triangle_size) * self.Width,
                                             (j + self.triangle_size) * self.Width,
                                             (i + 0.5) * self.Width, j * self.Width,
                                             fill="white", width=1)
        elif action == self.actions[1]:
            return self.board.create_polygon((i + 0.5 - self.triangle_size) * self.Width,
                                             (j + 1 - self.triangle_size) * self.Width,
                                             (i + 0.5 + self.triangle_size) * self.Width,
                                             (j + 1 - self.triangle_size) * self.Width,
                                             (i + 0.5) * self.Width, (j + 1) * self.Width,
                                             fill="white", width=1)
        elif action == self.actions[2]:
            return self.board.create_polygon((i + self.triangle_size) * self.Width,
                                             (j + 0.5 - self.triangle_size) * self.Width,
                                             (i + self.triangle_size) * self.Width,
                                             (j + 0.5 + self.triangle_size) * self.Width,
                                             i * self.Width, (j + 0.5) * self.Width,
                                             fill="white", width=1)
        elif action == self.actions[3]:
            return self.board.create_polygon((i + 1 - self.triangle_size) * self.Width,
                                             (j + 0.5 - self.triangle_size) * self.Width,
                                             (i + 1 - self.triangle_size) * self.Width,
                                             (j + 0.5 + self.triangle_size) * self.Width,
                                             (i + 1) * self.Width, (j + 0.5) * self.Width,
                                             fill="white", width=1)

    def render_grid(self, x, y, specials, walls):
        for i in range(x):
            for j in range(y):
                self.board.create_rectangle(i * self.Width, j * self.Width, (i + 1) * self.Width, (j + 1) * self.Width,
                                            fill="white", width=1)
                temp = {}
                for action in self.actions:
                    temp[action] = self.create_triangle(i, j, action)
                    self.cell_scores[(i, j)] = temp
        for (i, j, c, w) in specials:
            self.board.create_rectangle(i * self.Width, j * self.Width, (i + 1) * self.Width, (j + 1) * self.Width,
                                        fill=c, width=1)
        for (i, j) in walls:
            self.board.create_rectangle(i * self.Width, j * self.Width, (i + 1) * self.Width, (j + 1) * self.Width,
                                        fill="black", width=1)

    def set_cell_score(self, state, action, val):
        triangle = self.cell_scores[state][action]
        green_dec = int(
            min(255, max(0, (val - self.cell_score_min) * 255.0 / (self.cell_score_max - self.cell_score_min))))
        green = hex(green_dec)[2:]
        red = hex(255 - green_dec)[2:]
        if len(red) == 1:
            red += "0"
        if len(green) == 1:
            green += "0"
        color = "#" + red + green + "00"
        self.board.itemconfigure(triangle, fill=color)

    def update_player(self, new_x, new_y):
        self.board.coords(self.me, new_x * self.Width + self.Width * 2 / 10, new_y * self.Width + self.Width * 2 / 10,
                          new_x * self.Width + self.Width * 8 / 10,
                          new_y * self.Width + self.Width * 8 / 10)

    def restart_game(self, player):
        logger.debug('Game has restarted')
        self.board.coords(
            self.me,
            player[0] * self.Width + self.Width * 2 / 10,
            player[1] * self.Width + self.Width * 2 / 10,
            player[0] * self.Width + self.Width * 8 / 10,
            player[1] * self.Width + self.Width * 8 / 10
        )

    def start_game(self):
        logger.info('Tk mainloop started')
        master.mainloop()

    def stop_game(self):
        logger.info('Stopping display')
        master.quit()