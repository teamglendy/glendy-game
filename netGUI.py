import pygame as pg
import math
import sys
import socket

host = 'ir.cloud9p.org'
port = 1768
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.settimeout(0.1)

player = ''
n_rows = 11
n_columns = 11
glenda = (5, 5)
board_state = [[0 for i in range(11)] for i in range(11)]
done = False

circle_color = (0, 0, 255)
glenda_color = (0, 255, 0)
block_color = (255, 0, 0)

size = (625, 550)
circle_diameter = size[1]/11
circle_radius = circle_diameter/2
offset = circle_radius/5

def glenda_around(glenda):
    if glenda[0] % 2 == 0:
        around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1]),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]-1), (glenda[0]+1, glenda[1]-1)]
    else:
        around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]+1), (glenda[0]+1, glenda[1]+1),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1])]
    return around

def draw_board():
    y = circle_radius
    for c in range(n_columns):
        x = circle_radius
        if c%2!=0:
            x += circle_radius
        for r in range(n_rows):
            if board_state[c][r] == 0:
                pg.draw.circle(screen, circle_color, (x, y), circle_radius)
            elif board_state[c][r] == 1:
                pg.draw.circle(screen, block_color, (x, y), circle_radius)
            elif board_state[c][r] == 2:
                pg.draw.circle(screen, glenda_color, (x, y), circle_radius)
            x += circle_diameter+offset
        y += circle_diameter
    pg.display.update()

pg.init()
screen = pg.display.set_mode(size)
screen.fill((255, 255, 255))
draw_board()

def get_event():
    while True:
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
                if column is not None and board_state[row][column] not in (1, 2):
                    return row, column
                
def do_move():
    row, column = get_event()
    if player == 'trapper':
        sock.send(f'p {column} {row}\n'.encode('utf-8'))
    elif player == 'glenda':
        around = glenda_around(glenda)
        while (row, column) not in around:
            row, column = get_event()
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
        sock.send(f'm {dir}\n'.encode('utf-8'))
    draw_board()

def play():
    global player, glenda, board_state, done
    while not done:
        try:
            msg = sock.recv(1024).decode()
        except:
            break
        cmds = msg.split('\n')
        cmds.pop()
        while len(cmds) > 0:
            cmd = cmds[0].split(' ')
            match cmd[0]:
                case 'CONN':
                    if cmd[1] == '0':
                        player = 'trapper'
                    elif cmd[1] == '1':
                        player = 'glenda'
                    pg.display.set_caption(f"Glendy - {player.upper()}")
                    pg.display.update()
                case 'w':
                    board_state[int(cmd[2])][int(cmd[1])] = 1
                case 'g':
                    board_state[int(cmd[2])][int(cmd[1])] = 2
                case 'SENT':
                    draw_board()
                case 'TURN':
                    do_move()
                case 'SYNC':
                    if int(cmd[1]) % 2 != 0:
                        board_state[int(cmd[3])][int(cmd[2])] = 1
                        draw_board()
                    elif int(cmd[1]) % 2 == 0:
                        around = glenda_around(glenda)
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
                        board_state[glenda[0]][glenda[1]] = 0
                        board_state[glenda_next[0]][glenda_next[1]] = 2
                        glenda = glenda_next
                        draw_board()
                case 'WALL':
                    print('Chosen location is blocked. Please try again.')
                    do_move()
                case 'GLND':
                    print('Glendy is in the Chosen location. Please try again.')
                    do_move()
                case 'DIE':
                    done = True
                    break
                case 'WON':
                    print('You won!')
                    done = True
                    break
                case 'LOST':
                    print('You lost.')
                    done = True
                    break
            cmds.remove(cmds[0])

def alive():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

while True:
	play()
	alive()