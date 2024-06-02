import pygame as pg
import math
import socket
from tkinter import messagebox
import time

class netGlendy():
    def __init__(self, player, server, scale):
        server = server.split(':')
        self.host = server[0]
        self.port = int(server[1])
        self.srv_err = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except:
            messagebox.showerror('Error', 'There was a problem connecting to the server.')
            self.srv_err = True
        if self.srv_err == False:
            self.sock.settimeout(0.1)

            self.player = ''
            self.n_rows = 11
            self.n_columns = 11
            self.glenda = (5, 5)
            self.board_state = [[0 for i in range(11)] for i in range(11)]
            self.done = False
            self.finish = False

            self.circle_color = (0, 0, 0)
            self.glenda_color = (0, 255, 0)
            self.block_color = (255, 0, 0)

            self.size = (scale*125, scale*110)
            self.circle_diameter = self.size[1]/11
            self.circle_radius = self.circle_diameter/2
            self.offset = self.circle_radius/5

            pg.display.init()
            pg.display.set_caption("Glendy")
            self.screen = pg.display.set_mode(self.size)
            self.screen.fill((255, 255, 255))
            self.draw_board()

    def glenda_around(self, glenda):
        if glenda[0] % 2 == 0:
            around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1]),
                    (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]-1), (glenda[0]+1, glenda[1]-1)]
        else:
            around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]+1), (glenda[0]+1, glenda[1]+1),
                    (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1])]
        return around

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
        pg.display.update()

    def get_event(self):
        while True:
            time.sleep(0.1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.finish = True
                    pg.display.quit()
                    return None, None
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
                    if column is not None and self.board_state[row][column] not in (1, 2):
                        return row, column
                    
    def do_move(self):
        row, column = self.get_event()
        if row != None:
            if self.player == 'trapper':
                self.sock.send(f'p {column} {row}\n'.encode('utf-8'))
            elif self.player == 'glenda':
                around = self.glenda_around(self.glenda)
                while (row, column) not in around:
                    row, column = self.get_event()
                idx = around.index((row, column))
                match idx:
                    case 0:
                        dir = 'E'
                    case 1:
                        dir = 'NE'
                    case 2:
                        dir = 'SE'
                    case 3:
                        dir = 'W'
                    case 4:
                        dir = 'NW'
                    case 5:
                        dir = 'SW'
                self.sock.send(f'm {dir}\n'.encode('utf-8'))
            self.draw_board()

    def play(self):
        while not self.done:
            try:
                msg = self.sock.recv(1024).decode()
            except:
                break
            cmds = msg.split('\n')
            cmds.pop()
            while len(cmds) > 0:
                cmd = cmds[0].split(' ')
                match cmd[0]:
                    case 'CONN':
                        if cmd[1] == '0':
                            self.player = 'trapper'
                            self.circle_color = (42, 98, 154)
                            self.glenda_color = (255, 218, 120)
                            self.block_color = (255, 127, 62)
                        elif cmd[1] == '1':
                            self.player = 'glenda'
                            self.circle_color = (1, 32, 78)
                            self.glenda_color = (254, 174, 111)
                            self.block_color = (2, 131, 145)
                        pg.display.set_caption(f"Glendy - {self.player.upper()}")
                        pg.display.update()
                    case 'w':
                        self.board_state[int(cmd[2])][int(cmd[1])] = 1
                    case 'g':
                        self.board_state[int(cmd[2])][int(cmd[1])] = 2
                    case 'SENT':
                        self.draw_board()
                    case 'TURN':
                        self.do_move()
                    case 'SYNC':
                        if int(cmd[1]) % 2 != 0:
                            self.board_state[int(cmd[3])][int(cmd[2])] = 1
                            self.draw_board()
                        elif int(cmd[1]) % 2 == 0:
                            around = self.glenda_around(self.glenda)
                            match cmd[2]:
                                case 'E':
                                    glenda_next = around[0]
                                case 'NE':
                                    glenda_next = around[1]
                                case 'SE':
                                    glenda_next = around[2]
                                case 'W':
                                    glenda_next = around[3]
                                case 'NW':
                                    glenda_next = around[4]
                                case 'SW':
                                    glenda_next = around[5]
                            self.board_state[self.glenda[0]][self.glenda[1]] = 0
                            self.board_state[glenda_next[0]][glenda_next[1]] = 2
                            self.glenda = glenda_next
                            self.draw_board()
                    case 'WALL':    # WALL and GLND are not gonna be reached.
                        self.do_move()
                    case 'GLND':
                        self.do_move()
                    case 'DIE':
                        self.done = True
                        break
                    case 'WON':
                        messagebox.showinfo('Win','You won!.')
                        self.done = True
                        break
                    case 'LOST':
                        messagebox.showinfo('Lose','Gameover.')
                        self.done = True
                        break
                cmds.remove(cmds[0])

    def alive(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finish = True
                pg.display.quit()
                return

    def start(self):
        while self.srv_err == False:
            self.play()
            if self.finish == True:
                break
            self.alive()
