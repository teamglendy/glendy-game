import socket

host = 'localhost'
port = 1768

n_rows = 11
n_columns = 11
glenda = (5, 5)
board_state = [[0 for i in range(11)] for i in range(11)]

def glenda_around(glenda):
    if glenda[0] % 2 == 0:
        around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1]),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]-1), (glenda[0]+1, glenda[1]-1)]
    else:
        around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]+1), (glenda[0]+1, glenda[1]+1),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1])]
    return around

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

def sock_init():
    msg = ''
    while True:
        msg = msg + sock.recv(1024).decode()
        if 'SENT' in msg:
            return msg

def arrange_board(stats):
    for stat in stats:
        if stat != '' and stat[0] == 'w':
            axis = stat.split(' ')
            board_state[int(axis[2])][int(axis[1])] = 1
        elif stat != '' and stat[0] == 'g':
            axis = stat.split(' ')
            board_state[int(axis[2])][int(axis[1])] = 2

base_stats = sock_init()
stats_list = base_stats.split('\n')
arrange_board(stats_list)
print(base_stats)
for i in range(11):
    print(board_state[i])

done = False

while not done:
    msg = sock.recv(1024).decode()
    lines = msg.split('\n')
    lines.pop()
    while len(lines) > 0:
        cmd = lines[0].split(' ')
        match cmd[0]:
            case 'WAIT':
                pass
            case 'TURN':
                x = input('Enter axis X of where you wish to block: ')
                y = input('Enter axis Y of where you wish to block: ')
                sock.send(f'p {x} {y}\n'.encode('utf-8'))
            case 'SYNC':
                if int(cmd[1]) % 2 != 0:
                    board_state[int(cmd[3])][int(cmd[2])] = 1
                    for i in range(11):
                        print(board_state[i])
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
                    for i in range(11):
                        print(board_state[i])
            case 'WALL':
                print('Chosen location is already blocked. Please try again.')
            case 'GLND':
                print('Glendy is in the Chosen location. Please try again.')
            case 'ERR':
                pass
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
        lines.remove(lines[0])