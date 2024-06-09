import pygame as pg
import math
import socket
from tkinter import messagebox
import time

class netGlendy():
    def __init__(self, name, player, server, scale, mode, theme):
        self.srv_err = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server = server.split(':')
            self.host = server[0]
            self.port = int(server[1])
            self.sock.connect((self.host, self.port))
        except:
            messagebox.showerror('Error', 'There was a problem connecting to the server.')
            self.srv_err = True
        if self.srv_err == False:
            self.sock.settimeout(0.1)

            self.name = name
            self.opname = ''
            self.player = player
            match player:
                case 'Trapper':
                    self.player_code = 0
                case 'Glenda':
                    self.player_code = 1
                case 'Random':
                    self.player_code = 2
            match mode:
                case 'Multiplayer':
                    self.mode = 0
                case 'Singleplayer':
                    self.mode = 1
            self.sock.send(f'{self.name} 0 {self.player_code} {self.mode}\n'.encode('utf-8'))

            self.n_rows = 11
            self.n_columns = 11
            self.glenda = (5, 5)
            self.board_state = [[0 for i in range(11)] for i in range(11)]
            self.done = False
            self.finish = False

            self.circle_color = (128, 128, 128)
            self.glenda_color = (0, 255, 0)
            self.block_color = (255, 0, 0)

            self.size = (scale*125, scale*110)
            self.circle_diameter = self.size[1]/11
            self.circle_radius = self.circle_diameter/2
            self.offset = self.circle_radius/5

            pg.display.init()
            icon = pg.image.load('glenda.png')
            pg.display.set_icon(icon)
            pg.display.set_caption(f"{self.player} - Finding opponent...")
            self.screen = pg.display.set_mode(self.size)
            if theme == 'Light':
                self.screen.fill((255, 255, 255))
            elif theme == 'Dark':
                self.screen.fill((0, 0, 0))
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
            if self.player == 'Trapper':
                self.sock.send(f'p {column} {row}\n'.encode('utf-8'))
            elif self.player == 'Glenda':
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
            if msg == '':
                pg.display.set_caption(f"{self.player} - Something went wrong.")
                messagebox.showerror('Error','Something went wrong. You can exit.')
                self.done = True
                break
            cmds = msg.split('\n')
            cmds.pop()
            while len(cmds) > 0:
                cmd = cmds[0].split(' ')
                match cmd[0]:
                    case 'UGUD':
                        self.sock.send('y\n'.encode('utf-8'))
                    case 'CONN':
                        if cmd[1] == '0':
                            self.player = 'Trapper'
                            self.circle_color = (42, 98, 154)
                            self.glenda_color = (255, 218, 120)
                            self.block_color = (255, 127, 62)
                        elif cmd[1] == '1':
                            self.player = 'Glenda'
                            self.circle_color = (33, 156, 144)
                            self.glenda_color = (229, 86, 4)
                            self.block_color = (233, 184, 36)
                        self.opname = cmd[2]
                        pg.display.update()
                    case 'w':
                        self.board_state[int(cmd[2])][int(cmd[1])] = 1
                    case 'g':
                        self.board_state[int(cmd[2])][int(cmd[1])] = 2
                    case 'SENT':
                        pg.display.set_caption(f"{self.player} - Opponent: {self.opname} - Opponent's turn, Please wait")
                        self.draw_board()
                    case 'TURN':
                        pg.display.set_caption(f"{self.player} - Opponent: {self.opname} - Your turn")
                        self.do_move()
                    case 'SYNC':
                        pg.display.set_caption(f"{self.player} - Opponent: {self.opname} - Opponent's turn, Please wait")
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
                    case 'ERR':
                        print(msg)
                    case 'DIE':
                        self.done = True
                        print(msg)
                        break
                    case 'WON':
                        pg.display.set_caption(f"{self.player} - You won, {self.name}! :)")
                        messagebox.showinfo('Win','You won!.')
                        self.done = True
                        break
                    case 'LOST':
                        pg.display.set_caption(f"{self.player} - You lost, {self.name}. :(")
                        messagebox.showinfo('Lose','Gameover.')
                        self.done = True
                        break
                cmds.remove(cmds[0])

    def alive(self):
        time.sleep(0.05)
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
