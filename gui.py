import pygame as pg
import math
import env
from tkinter import messagebox
import time

class Glendy():

    def __init__(self, difficulty):

        self.env = env.GlendyEnv()
        self.n_rows = 11
        self.n_columns = 11
        self.board_state = [[0 for i in range(11)] for i in range(11)]
        self.glenda = self.env.start
        self.board_state[self.glenda[0]][self.glenda[1]] = 2
        self.env.arrange_blocks(difficulty)
        for block in self.env.blocks:
            self.board_state[block[0]][block[1]] = 1        
        self.done = False

        self.circle_color = (42, 98, 154)
        self.glenda_color = (255, 218, 120)
        self.block_color = (255, 127, 62)

        self.size = (625, 550)
        self.circle_diameter = self.size[1]/11
        self.circle_radius = self.circle_diameter/2
        self.offset = self.circle_radius/5

        pg.display.init()
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill((255, 255, 255))
        pg.display.set_caption("Glendy")
        self.draw_board()
        pg.display.update()

    def draw_board(self):
        y = self.circle_radius
        for c in range(self.n_columns):
            x = self.circle_radius
            if c%2!=0:
                x += self.circle_radius
            for r in range(self.n_rows):
                if self.board_state[c][r] == 0:
                    pg.draw.circle(self.screen, self.circle_color, (x, y), self.circle_radius)
                elif self.board_state[c][r] == 1:
                    pg.draw.circle(self.screen, self.block_color, (x, y), self.circle_radius)
                elif self.board_state[c][r] == 2:
                    pg.draw.circle(self.screen, self.glenda_color, (x, y), self.circle_radius)
                x += self.circle_diameter+self.offset
            y += self.circle_diameter

    def start(self):
        while not self.done:
            time.sleep(0.1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    return
                if event.type == pg.MOUSEBUTTONDOWN:
                    x_axis = event.pos[0]
                    y_axis = event.pos[1]
                    row = math.floor(y_axis/self.circle_diameter)
                    if row % 2 != 0:
                        if x_axis >= self.circle_radius:
                            column = math.floor((x_axis-self.circle_radius)/(self.circle_diameter+self.offset))
                        else:
                            column = None
                    else:
                        if x_axis <= self.size[0]-self.circle_radius:
                            column = math.floor(x_axis/(self.circle_diameter+self.offset))
                        else:
                            column = None
                    if column is not None and (row, column) not in self.env.blocks and (row, column) != self.glenda:
                        self.board_state[row][column] = 1
                        self.env.blocks.append((row, column))
                        if (row, column) in self.env.exits:
                            self.env.exits.remove((row, column))
                        glenda_next = self.env.get_glenda_move(self.glenda)
                        if self.env.result == "win":
                            self.draw_board()
                            pg.display.update()
                            messagebox.showinfo('Win','You Won!')
                            pg.display.quit()
                            return
                        self.board_state[self.glenda[0]][self.glenda[1]] = 0
                        self.board_state[glenda_next[0]][glenda_next[1]] = 2
                        self.glenda = glenda_next
                    self.draw_board()
                    pg.display.update()
                    self.env.check_lose(self.glenda)
                    if self.env.result == "lose":
                        messagebox.showinfo('Lose','Gameover.')
                        pg.display.quit()
                        return

