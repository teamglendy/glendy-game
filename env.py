import random
import glendaAI

glenda_ai = glendaAI.bfs()

class GlendyEnv():

  rows = 11
  columns = 11
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

  def arrange_blocks(self, difficulty):
    self.blocks.clear()
    if difficulty == 'Easy':
      num_blocks = random.randint(10, 15)
    elif difficulty == 'Medium':
      num_blocks = random.randint(5, 10)
    elif difficulty == 'Hard':
      num_blocks = random.randint(1, 5)
    elif difficulty == 'Impossible':
       num_blocks = 0
    for i in range(num_blocks):
      row = random.randint(0, 10)
      column = random.randint(0, 10)
      if (row, column) not in self.blocks and (row, column) != (5, 5):
        self.blocks.append((row, column))
      else: i-=1
    for block in self.blocks:
      if block in self.exits:
        self.exits.remove(block)

  def reset_state(self): # extra
    self.exits = self.base_exits.copy()
    self.blocks.clear()
    self.arrange_blocks()
    state = [[0 for i in range(11)] for i in range(11)]
    for block in self.blocks:
      state[block[0]][block[1]] = -1
    state[self.start[0]][self.start[1]] = 1
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

  def check_lose(self, glenda_next):
    if glenda_next in self.exits:
      self.result = "lose"
