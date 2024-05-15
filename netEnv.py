import socket

class netGlendy():

    def __init__(self, player): 
        self.host = 'localhost'
        self.port = 1768
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.player = player
        self.n_rows = 11
        self.n_columns = 11
        self.glenda = (5, 5)
        self.board_state = [[0 for i in range(11)] for i in range(11)]
        self.done = False
        
    def glenda_around(self, glenda):
        if glenda[0] % 2 == 0:
            around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1]),
                    (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]-1), (glenda[0]+1, glenda[1]-1)]
        else:
            around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]+1), (glenda[0]+1, glenda[1]+1),
                    (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1])]
        return around

    def sock_init(self):
        msg = ''
        while True:
            msg = msg + self.sock.recv(1024).decode()
            if 'SENT' in msg:
                return msg

    def arrange_board(self, stats):
        for stat in stats:
            if stat != '' and stat[0] == 'w':
                axis = stat.split(' ')
                self.board_state[int(axis[2])][int(axis[1])] = 1
            elif stat != '' and stat[0] == 'g':
                axis = stat.split(' ')
                self.board_state[int(axis[2])][int(axis[1])] = 2

    def server(self, cmds, x=0, y=0, dir=''):
        while len(cmds) > 0:
            cmd = cmds[0].split(' ')
            match cmd[0]:
                case 'WAIT':
                    pass
                case 'TURN':
                    if self.player == 'trapper':
                        self.sock.send(f'p {x} {y}\n'.encode('utf-8'))
                    elif self.player == 'glenda':
                        self.sock.send(f'm {dir}\n'.encode('utf-8'))
                case 'SYNC':
                    if int(cmd[1]) % 2 != 0:
                        self.board_state[int(cmd[3])][int(cmd[2])] = 1
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
                case 'WALL':
                    print('Chosen location is blocked. Please try again.')
                case 'GLND':
                    print('Glendy is in the Chosen location. Please try again.')
                case 'ERR':
                    pass
                case 'DIE':
                    self.done = True
                    break
                case 'WON':
                    print('You won!')
                    self.done = True
                    break
                case 'LOST':
                    print('You lost.')
                    self.done = True
                    break
            cmds.remove(cmds[0])