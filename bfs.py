'''
*******************Developed by********************************
    
Alfredo Albelis Batista Filho - https://github.com/AlfredoFilho
Brenda Alexsandra Januario - https://github.com/brendajanuario
Cleofas Peres Santos - https://github.com/CleoPeres

**************************************************************** 
'''

class cat():
    cat    = ()
    blocks = []
    exits  = []

    positionCat = ()
    chosen_exit = exits
    positionCatInTuple = tuple(cat)
    positionsVisited = []
    expandedStates = []

    def next_move(self, direction, cat) :
        candidatos = {
            "NW": [(cat[0]-1, cat[1]-1), (cat[0]-1, cat[1])],
            "NE": [(cat[0] - 1, cat[1]), (cat[0]-1, cat[1] + 1)],
            "W" : [(cat[0], cat[1] - 1), (cat[0], cat[1] - 1)],
            "E" : [(cat[0], cat[1] + 1), (cat[0], cat[1] + 1)],
            "SW": [(cat[0] + 1, cat[1] - 1),(cat[0] + 1, cat[1])],
            "SE": [(cat[0] + 1, cat[1]),(cat[0] + 1, cat[1]+1)]
        }
        return candidatos[direction][cat[0]%2]

    def BreadthFirstSearch (self, cat, chosen_exit, blocks):

        solutionFound = False
        self.positionsVisited.append(cat) #add cat position in list of positions visited
        
        while len(self.positionsVisited) != 0:
            atual = self.positionsVisited.pop(0) #remove first of list
            if(atual not in blocks and atual in chosen_exit):
                solutionFound = True
                break
            successorStates = self.findSuccessorPositions(atual, self.expandedStates, self.positionsVisited) #call function to walk with the cat and find the next positions
            self.expandedStates.append(atual)

            for i in range (0, len(successorStates)): #check the new positions to see if they have already been included
                successor = successorStates[i]
                if successor not in self.expandedStates and successor not in self.positionsVisited:
                    self.positionsVisited.append(successorStates[i])
    
        if solutionFound == True:
            movimento = self.Solution(atual)
            del self.expandedStates[:]
            del self.positionsVisited[:]
            del successorStates[:]
            # print(movimento[-1])
        try:
            return movimento[-1]
        except:
            return "win"
        
    predecessorCoordinates={}
    predecessorPosition={}

    def findSuccessorPositions(self, cat, expandedStates, positionsVisited):
        coordinates = ["NE","E","SW","SE","W","NW"]
        successorPositions=[]
        for el in coordinates:
            successor = self.next_move(el, cat)
            if (successor[0]<0 or successor[1]<0 or successor[0]>10 or successor[1]>10):
                continue
            elif(successor in self.blocks):
                continue
            elif(successor not in expandedStates and successor not in positionsVisited and successor not in self.blocks):
                successorPositions.append(successor)
                self.predecessorCoordinates[successor]=el
                self.predecessorPosition[successor]=cat
        
        return successorPositions
        
    def Solution(self, cat):
        listPositions=[]
        listCoordinates=[]
        aux=cat
        listPositions.append(cat)
        while (aux != tuple(self.positionCat)):
            listPositions.append(self.predecessorPosition[aux])
            listCoordinates.append(self.predecessorCoordinates[aux])
            aux = self.predecessorPosition[aux]
        return listCoordinates

    # BreadthFirstSearch(positionCatInTuple, chosen_exit, blocks)