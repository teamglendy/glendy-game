'''
*******************Developed by********************************
    
Alfredo Albelis Batista Filho - https://github.com/AlfredoFilho
Brenda Alexsandra Januario - https://github.com/brendajanuario
Cleofas Peres Santos - https://github.com/CleoPeres

**************************************************************** 
'''

class bfs():
    glenda = ()
    blocks = []
    exits  = []

    positionGlenda = ()
    chosen_exit = exits
    positionsVisited = []
    expandedStates = []

    def next_move(self, direction, glenda) :
        candidates = {
            "nw": [(glenda[0]-1, glenda[1]-1), (glenda[0]-1, glenda[1])],
            "ne": [(glenda[0] - 1, glenda[1]), (glenda[0]-1, glenda[1] + 1)],
            "w" : [(glenda[0], glenda[1] - 1), (glenda[0], glenda[1] - 1)],
            "e" : [(glenda[0], glenda[1] + 1), (glenda[0], glenda[1] + 1)],
            "sw": [(glenda[0] + 1, glenda[1] - 1),(glenda[0] + 1, glenda[1])],
            "se": [(glenda[0] + 1, glenda[1]),(glenda[0] + 1, glenda[1]+1)]
        }
        return candidates[direction][glenda[0]%2]

    def BreadthFirstSearch (self, glenda, chosen_exit, blocks):

        solutionFound = False
        self.positionsVisited.append(glenda) #add glenda position in list of positions visited
        
        while len(self.positionsVisited) != 0:
            current = self.positionsVisited.pop(0) #remove first of list
            if(current not in blocks and current in chosen_exit):
                solutionFound = True
                break
            successorStates = self.findSuccessorPositions(current, self.expandedStates, self.positionsVisited) #call function to walk with the glenda and find the next positions
            self.expandedStates.append(current)

            for i in range (0, len(successorStates)): #check the new positions to see if they have already been included
                successor = successorStates[i]
                if successor not in self.expandedStates and successor not in self.positionsVisited:
                    self.positionsVisited.append(successorStates[i])
    
        if solutionFound == True:
            movement = self.Solution(current)
            del self.expandedStates[:]
            del self.positionsVisited[:]
            del successorStates[:]
        try:
            return movement[-1]
        except:
            return "win"
        
    predecessorCoordinates={}
    predecessorPosition={}

    def findSuccessorPositions(self, glenda, expandedStates, positionsVisited):
        coordinates = ["ne","e","sw","se","w","nw"]
        successorPositions=[]
        for el in coordinates:
            successor = self.next_move(el, glenda)
            if (successor[0]<0 or successor[1]<0 or successor[0]>10 or successor[1]>10):
                continue
            elif(successor in self.blocks):
                continue
            elif(successor not in expandedStates and successor not in positionsVisited and successor not in self.blocks):
                successorPositions.append(successor)
                self.predecessorCoordinates[successor]=el
                self.predecessorPosition[successor]=glenda
        
        return successorPositions
        
    def Solution(self, glenda):
        listPositions=[]
        listCoordinates=[]
        aux=glenda
        listPositions.append(glenda)
        while (aux != tuple(self.positionGlenda)):
            listPositions.append(self.predecessorPosition[aux])
            listCoordinates.append(self.predecessorCoordinates[aux])
            aux = self.predecessorPosition[aux]
        return listCoordinates