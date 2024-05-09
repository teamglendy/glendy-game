import pygame as pg
import math
import sys
import numpy as np
import env
from tkinter import messagebox

env = env.Glendy()

n_rows = 11
n_columns = 11
board_state = np.zeros((n_rows, n_columns))
glenda = env.start
board_state[glenda] = 2
env.arrange_blocks()
for tp in env.blocks:
    board_state[tp] = 1

circle_color = (0, 0, 255)
glenda_color = (0, 255, 0)
block_color = (255, 0, 0)

size = (1250, 1100)
circle_diameter = size[1]/11
circle_radius = circle_diameter/2
offset = circle_radius/5

def draw_board():
    y = circle_radius
    for c in range(n_columns):
        x = circle_radius
        if c%2!=0:
            x += circle_radius
        for r in range(n_rows):
            if board_state[c, r] == 0:
                pg.draw.circle(screen, circle_color, (x, y), circle_radius)
            elif board_state[c, r] == 1:
                pg.draw.circle(screen, block_color, (x, y), circle_radius)
            elif board_state[c, r] == 2:
                pg.draw.circle(screen, glenda_color, (x, y), circle_radius)
            x += circle_diameter+offset
        y += circle_diameter

pg.init()
screen = pg.display.set_mode(size)
screen.fill((255, 255, 255))
pg.display.set_caption("Glendy")
draw_board()
pg.display.update()

done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            x_axis = event.pos[0]
            y_axis = event.pos[1]
            row = math.floor(y_axis/circle_diameter)
            if row % 2 != 0:
                if x_axis >= circle_radius:
                    column = math.floor((x_axis-circle_radius)/(circle_diameter+offset))
                else:
                    column = None
            else:
                if x_axis <= size[0]-circle_radius:
                    column = math.floor(x_axis/(circle_diameter+offset))
                else:
                    column = None
            if column is not None and (row, column) not in env.blocks and (row, column) != glenda:
                board_state[row, column] = 1
                env.blocks.append((row, column))
                if (row, column) in env.exits:
                    env.exits.remove((row, column))
                glenda_next = env.get_glenda_move(glenda)
                if env.result == "win":
                    draw_board()
                    pg.display.update()
                    messagebox.showinfo('Exit','You Won!')
                    sys.exit()
                board_state[glenda] = 0
                board_state[glenda_next] = 2
                glenda = glenda_next
            draw_board()
            pg.display.update()
            env.check_lose(glenda)
            if env.result == "lose":
                messagebox.showinfo('Exit','Gameover.')
                sys.exit()
            print(board_state)

