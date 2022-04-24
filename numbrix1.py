# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 06:
# 96868 Guilherme Carvalho
# 96884 José Mateus


import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search
import time
import debugpy



actionsCounter = 0 # represents how many actions were generated
timeListVer = []
timeListHor = []

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

        self.parentId = 0

        self.lastPlacedNumber = -1
        self.isIncreasing = 1 # used to know if numbers increasing or decreasing. has to be passed from father state to child state


    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, boardList=None, filledSquares=None):
        
        # The board will contain two representations that will be used in different places
        # one will be a list of lists mostly used for the neighbors
        # one will be a dict, where the key corresponds to a placed number and the value corresponds to a list of [x,y]
        

        if boardList == None: 
            # if I receive a board, I will also receive a boardSize
            
            self.filledSquares = 0
            self.board = []
            self.boardSize = 0
            self.boardDict = {}
            return
        
        # Board will be represeented as a list of lists
        # this boardList that I am receiving I will need to create my own copy manually
        self.boardSize = len(boardList)
        self.board = [[value for value in row] for row in boardList]
        self.createDict()
        # print("Setting filled squares ", filledSquares)
        self.filledSquares = filledSquares


    def getRawBoard(self):
        """" Devolve o estado em que a Board esta, sendo este a lista de listas representado o board e o numero de posicoes preenchidas """
        return self.board.copy(), self.filledSquares
    
        
    def makeAction(self, action: (int, int, int)): #  row: int, col: int, value: int):
        """ Recebe um tuplo com: uma linha, uma coluna e um valor, e mete esse valor na posicao dada  """      
        # print("this is the action ", action)
        self.board[action[0]][action[1]] = action[2]
        
        # [check] - sera que aqui nao tenho que verificar se isto e uma acao valida
        self.boardDict[action[2]] = [action[0], action[1]]
        return

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente acima e abaixo, 
        respectivamente. """
        
        if row == 0:
            return (-1,self.board[row+1][col])
        if row == self.boardSize-1:
            return (self.board[row-1][col],-1)
        
        return (self.board[row-1][col], self.board[row+1][col])
        

        # se for 0 quer dizer que e uma posicao valida mas nao tem nada la
        # se for -1 quer dizer que e uma parede
        #   high vai ser menos 1 quando row = 0
        # se for qualquer outro numero quer dizer que esse numero esta la 
        # basicamente eu vou percorrer o meu dicionario e ver se la nao encontro os valores acima ou abaixo

    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        
        if col == 0:
            return (-1,self.board[row][col+1])
        if col == self.boardSize-1:
            return (self.board[row][col-1],-1)
        return (self.board[row][col-1], self.board[row][col+1])


    def createDict(self):
        """
        Receives a list that represents a board and generates a dictionary with that board
        """
        self.boardDict = {}
      

        for rowIndex in range(len(self.board)):
            col = self.board[rowIndex]
            for colIndex in range(len(col)):
                if (value := col[colIndex]) != 0:
                    self.boardDict[value] = [rowIndex, colIndex]
                    

        # for line in self.board:
        #     for value in line:
        #         if value != 0:
        #             #entao vou querer adicionar ao dict
        #             self.boardDict[value] = [self.board.index(line), line.index(value)]

    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
    
        # Create the board object
        myBoard = Board()
        with open(filename,"r") as f:

            # Read the size of the board
            myBoard.boardSize = int(f.readline())

            # Read the whole board
            lines = f.readlines()

            
            
            for lineIndex in range(len(lines)):
                numberList = lines[lineIndex].split("\t")
                tempList = []
                
                for numberIndex in range(len(numberList)):
                
                    if (value := int(numberList[numberIndex])) != 0:
                        myBoard.boardDict[value] = [lineIndex, numberIndex]
                        myBoard.filledSquares += 1          
                    tempList.append(value)
                
                myBoard.board.append(tempList)
                
            # sumList = []
            # for line in lines:
            #     numberList = line.split("\t")
            #     myBoard.board.append([int(x) for x in numberList])
            #     sumList = [1 for x in numberList if int(x) != 0 ]
            #     myBoard.filledSquares += sum(sumList)

        return myBoard

    def __repr__(self):
        myString = ""

        for line in self.board:
            for number in line:
                myString = myString +  f"{number}\t"
            
            myString += "\n"
        
        return myString[:-1]

    


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.currentState = NumbrixState(board)
        self.originalState = self.currentState
        super().__init__(self.currentState)
        

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        global actionsCounter

        # eu vou querer tentar mais duas coisas
        # vou querer tentar fazer do max para baixo e depois max para cima
        # e vou querer tentar fazer do min para cima e depois min para baixo

        # vamos primeiro a cada numero colocado, ver os vizinhos e criar estados em que os vizinhos sao todos os os numeros adjacentes
        # para isto se calhar vou querer ter um dicionario de numeros ja colocados e as posicoes deles mas por enquanto nao vou fazer isso
        
        # get the dict of placed numbers THIS CAN BE OPTIMIZED (prob create a list)
        
        stateList = []
        
        # mudar isto
        myBoard = state.board
        
        # vamos preencher isto tipo uma cobra, vou pegar no maximo preencher os vizinhos e fazer isso ate chegar ao fim
        # depois vou pegar no meu max inicial e vou comecar a preencher para baixo e verificar se os numeros que estou a meter cabem
        # vou ter uns problemas com isto depois quando voltar para o min, na verdade eu quero voltar para o max inicial mas depois penso nisto
        
        
        
        print("This is the board")
        print(state.board)

        if state.lastPlacedNumber == -1:
            # quer dizer que e a minha primeira iteracao e quero escolher o valor minimo
            choosenNumber = min(myBoard.boardDict.keys())
        else:
            # ja nao estou na minha primeira itereacao
            # entao eu vou querer escolher o lastPlacedNumber + 1
            # mas se o lastPlacedNumber + 1 for o maximo, entao eu vou querer escolher o min e comecar a diminuir
            choosenNumber = state.lastPlacedNumber


        while(choosenNumber + state.isIncreasing in state.board.boardDict.keys()):
            choosenNumber = choosenNumber + state.isIncreasing

        if(choosenNumber == myBoard.boardSize*myBoard.boardSize):
            # isto quer dizer que ja coloquei o ultimo numero para cima, entao vamos voltar ao min e comecar a colocar para baixo
            # print("I have reached the max")
            state.isIncreasing = -1
            choosenNumber = min(myBoard.boardDict.keys())

         
        adjacentPostions = myBoard.adjacent_vertical_numbers(myBoard.boardDict[choosenNumber][0], myBoard.boardDict[choosenNumber][1]) + myBoard.adjacent_horizontal_numbers(myBoard.boardDict[choosenNumber][0], myBoard.boardDict[choosenNumber][1])
        neighborOrder = [[-1,0], [1, 0], [0, -1], [0, 1]]  # order that  I will be looking at the neighbors up, down, left, right
        
        for x in range(len(neighborOrder)):
            if adjacentPostions[x] != 0:
                # means that there is either a wall or a number in that position
                # in that case I do not want to fill it
                continue
        
            # vou querer meter o choosenNumber + 1 para os vizgit add .inhos
            myPos = [element1 + element2 for (element1, element2) in zip(myBoard.boardDict[choosenNumber], neighborOrder[x])]
            stateList.append( ( myPos[0], myPos[1], choosenNumber + state.isIncreasing ) )

            

        actionsCounter += len(stateList)

        print(f"THis is the parent ID {state.parentId} and this is my id {state.id}")
        print(f"Choosen number {choosenNumber} placed number {choosenNumber+state.isIncreasing} isIncreasing {state.isIncreasing}")
        print("This is the aciton list  ", stateList)
        print( )
        return stateList



    def result(self, state: NumbrixState, action: (int, int, int)):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        # print("This is result with this action type ", action, " and this is the new board:")
        # I will want to create a new state, not edit the old one



        # Create the newState
        # boardRepresent, filledSquare = state.board.getRawBoard()
        newBoard = Board(state.board.board, state.board.filledSquares)
        newState = NumbrixState(newBoard)
        # Update new state
        newBoard.makeAction(action)
        newState.board.filledSquares+=1

        # print(action)
        # print("prev")
        # print(state.board)
        # print("new")
        # print(newBoard)
        # print()

        # print("updating last placed number to ", action[2])
        newState.lastPlacedNumber = action[2]
        newState.isIncreasing = state.isIncreasing
        newState.parentId = state.id

        return newState

    
    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """


        # ver se tenho todos os numeros colocados com o filledSquares (poupar loop)

        # Check if all numbers have been filled
        if state.board.filledSquares != state.board.boardSize*state.board.boardSize:
            # print("This was false")
            return False
        
        # vou dict[n] e vejo se a posicao e vizinha do dict[n+1]
        # ver 1 com 2, 2 com 3, 3 com 4
        for number in range(1, state.board.boardSize*state.board.boardSize):
            if not self.isNeighbour(state.board.boardDict[number], state.board.boardDict[number+1]):
                # print("This was false")
                return False
        
        # print("This was true")
        return True


    def isNeighbour(self, p1, p2):
        """
        Receives two positions consisting of [x,y] and returns true if p1 and p2 are neighbours
        """
        # esta funcao esta a deixar passar valores na diagonal
        return abs(p1[0]-p2[0]) <= 1 and abs(p1[1]-p2[1]) <= 1 


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":

    # check for debug flag
    if len(sys.argv) > 2:
        debugpy.listen(5678)
        print("Waiting for debugger attach")
        debugpy.wait_for_client()


    # Ler o ficheiro de input de sys.argv[1],
    myBoard = Board.parse_instance(sys.argv[1])

    start = time.time()
    
    # Usar uma técnica de procura para resolver a instância,
    myProblem = Numbrix(myBoard)

    # Retirar a solução a partir do nó resultante,
    objective = depth_first_tree_search(myProblem)

    # objective = breadth_first_tree_search(myProblem)

    # Imprimir para o standard output no formato indicado.
    print("The solution is:\n", objective.state.board, sep="")
    end = time.time()
    print("It took: ", end - start)
    
    print(f"Did this amount of acitons {actionsCounter}")

