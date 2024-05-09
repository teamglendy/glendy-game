import numpy
import random
import glendaAI

glenda_ai = glendaAI.bfs()

class Glendy():

  start = (5, 5)
  blocks = []
  base_exits = [
         (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
         (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0),
         (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
         (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10)
               ]
  exits = base_exits.copy()
  actions = ['ne', 'e', 'se', 'nw', 'w', 'sw']
  result = ""

  def arrange_blocks(self):
    self.blocks.clear()
    num_blocks = random.randint(5, 20)
    for i in range(num_blocks):
      row = random.randint(0, 10)
      column = random.randint(0, 10)
      if (row, column) not in self.blocks and (row, column) != (5, 5):
        self.blocks.append((row, column))
      else: i-=1
    for tp in self.blocks:
      if tp in self.exits:
        self.exits.remove(tp)

  def reset_state(self):
    self.exits = self.base_exits.copy()
    self.blocks.clear()
    self.arrange_blocks()
    state = numpy.zeros((11, 11))
    for tp in self.blocks:
      state[tp] = -1
    state[self.start] = 1
    return state
  
  def glenda_around(self, glenda):
    if glenda[0] % 2 == 0:
      around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1]),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]-1), (glenda[0]+1, glenda[1]-1)]
    else:
      around = [(glenda[0], glenda[1]+1), (glenda[0]-1, glenda[1]+1), (glenda[0]+1, glenda[1]+1),
                (glenda[0], glenda[1]-1), (glenda[0]-1, glenda[1]), (glenda[0]+1, glenda[1])]
    return around

  def get_glenda_move(self, glenda):
    while True:
      glenda_ai.blocks = self.blocks
      glenda_ai.positionGlenda = glenda
      glenda_move = glenda_ai.BreadthFirstSearch(glenda, self.exits, self.blocks)
      around = self.glenda_around(glenda)
      match glenda_move:
        case 'e':
            glenda_next = around[0]
        case 'ne':
            glenda_next = around[1]
        case 'se':
            glenda_next = around[2]
        case 'w':
            glenda_next = around[3]
        case 'nw':
            glenda_next = around[4]
        case 'sw':
            glenda_next = around[5]
        case 'win':
            glenda_next = glenda
            self.result = 'win'
      if (glenda_next not in self.blocks):
        return glenda_next
  
  def check_win(self, glenda):
    pass
    # self.result = "win"

  def check_lose(self, glenda_next):
    if glenda_next in self.exits:
      self.result = "lose"
