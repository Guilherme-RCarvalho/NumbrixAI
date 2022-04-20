# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 06:
# 96868 Guilherme Carvalho
# 96884 José Mateus

import sys
import copy
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, board=None, filledSquares=None):
        
        if board == None: 
            # if I receive a board, I will also receive a boardSize
            
            self.filledSquares = 0
            self.board = []
            self.boardSize = 0

            return
        

        # Board will be represeented as a list of lists
        self.boardSize = len(board)
        self.board = board
        self.filledSquares = filledSquares
        
    def getRawBoard(self):
        """" Devolve o estado em que a Board esta, sendo este a lista de listas representado o board e o numero de posicoes preenchidas """
        return self.board.copy(), self.filledSquares
    
        
    def makeAction(self, action: (int, int, int)): #  row: int, col: int, value: int):
        """ Recebe um tuplo com: uma linha, uma coluna e um valor, e mete esse valor na posicao dada  """      
        self.board[action[0]][action[1]] = action[2]
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
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        
        if col == 0:
            return (-1,self.board[row][col+1])
        if col == self.boardSize-1:
            return (self.board[row][col-1],-1)
        return (self.board[row][col-1], self.board[row][col+1])
    
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

            sumList = []

            for line in lines:
                numberList = line.split("\t")
                myBoard.board.append([int(x) for x in numberList])
                sumList = [1 for x in numberList if int(x) != 0 ]
                myBoard.filledSquares += sum(sumList)


           


        return myBoard

    def __repr__(self):
        myString = ""

        for line in self.board:
            for number in line:
                myString = myString +  f" {number}"
            myString += "\n"
        
        return myString[:-1]

    # TODO: outros metodos da classe

    


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.currentState = NumbrixState(board)
        self.originalState = self.currentState
        super().__init__(self.currentState)

        self.possibleStates = [] # To be filled with all the states that can be reach from the current state
        
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        
        # vamos primeiro a cada numero colocado, ver os vizinhos e criar estados em que os vizinhos sao todos os os numeros adjacentes
        # para isto se calhar vou querer ter um dicionario de numeros ja colocados e as posicoes deles mas por enquanto nao vou fazer isso
        
        # get the dict of placed numbers THIS CAN BE OPTIMIZED (prob create a list)

        myBoard, _ = state.board.getRawBoard()
        stateList = []
        
        
        placedValuesDict = {} 
        for row in myBoard:
            for value in row:
                if value != 0:
                    placedValuesDict[value] = [myBoard.index(row), row.index(value)]
    

        # mudar isto
        myBoard = state.board

        # for each placed value (in incrementing order) 
        neighborOrder = [[-1,0], [1, 0], [0, -1], [0, 1]]  # order that  I will be looking at the neighbors up, down, left, right
        for value in sorted(placedValuesDict.keys()):
            # pegar os adjacentes para os lados e para cima da posicao do numero colocado
            adjacentPostions = myBoard.adjacent_vertical_numbers(placedValuesDict[value][0], placedValuesDict[value][1]) + myBoard.adjacent_horizontal_numbers(placedValuesDict[value][0], placedValuesDict[value][1])

            for x in range(len(neighborOrder)):

                if adjacentPostions[x] != 0:
                    continue
            
                # means that I will want to create a new state (possible two) where the possition is neighborOrder[x]
                # check if i need two states or one state (only need one state if the value is 1 or the value is max)
                if value == 1:
                    changeNumberList = [1]
                elif value == myBoard.boardSize*myBoard.boardSize:
                    changeNumberList = [-1]
                else:
                    changeNumberList = [1, -1]
                
                for incrimentValue in changeNumberList:
                    
                    # i dont want to add a number that is already on the board
                    if value + incrimentValue in placedValuesDict.keys():
                        continue

                    myPos = [element1 + element2 for (element1, element2) in zip(placedValuesDict[value], neighborOrder[x])]
                    stateList.append((myPos[0], myPos[1], value + incrimentValue))
            
        return stateList



    def result(self, state: NumbrixState, action: (int, int, int)):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        # print("This is result with this action type ", action, " and this is the new board:")
        # I will want to create a new state, not edit the old one

        # Create the newState
        boardRepresent, filledSquare = state.board.getRawBoard()
        newBoard = Board(copy.deepcopy(boardRepresent), filledSquare)
        newState = NumbrixState(newBoard)
        # Update new state
        newBoard.makeAction(action)
        newState.board.filledSquares+=1

        print(action)
        print("prev")
        print(state.board)
        print("new")
        print(newBoard)
        print()

        
        return newState

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """


        # print("Testing this board")
        # print(state.board)
        myBoard, _ = state.board.getRawBoard()

        
        placedValuesDict = {} 
        for row in myBoard:
            for value in row:
                if value != 0:
                    placedValuesDict[value] = [myBoard.index(row), row.index(value)]

        # TODO modify after
        myBoard = state.board


        # ver se tenho todos os numeros colocados com o filledSquares (poupar loop)

        # Check if all numbers have been filled
        if state.board.filledSquares != state.board.boardSize*state.board.boardSize:
            # print("This was false")
            return False

        # vou dict[n] e vejo se a posicao e vizinha do dict[n+1]
        # ver 1 com 2, 2 com 3, 3 com 4
        for number in range(1, state.board.boardSize*state.board.boardSize-1):
            if not self.isNeighbour(placedValuesDict[number], placedValuesDict[number+1]):
                # print("This was false")
                return False
        
        # print("This was true")
        return True

            

        # sera que as keys do meu dicionario vao estar ordenados

        # if state.board.filledSquares == state.board.boardSize*state.board.boardSize:
        #     print("hello")
        #     for key in range(1,state.board.boardSize*state.board.boardSize):
        #         print("this is the key", key)
        #         print(myBoard.adjacent_vertical_numbers(placedValuesDict[key+1][0], placedValuesDict[key+1][1]))
        #         if key in myBoard.adjacent_vertical_numbers(placedValuesDict[key+1][0], placedValuesDict[key+1][1]) or key in myBoard.adjacent_horizontal_numbers(placedValuesDict[key+1][0], placedValuesDict[key+1][1]):
        #             print("im here")
        #             continue
        #         else:
        #             return False
        #     return True
        # return False

    def isNeighbour(self, p1, p2):
        """
        Receives two positions consisting of [x,y] and returns true if p1 and p2 are neighbours
        """
         
        return abs(p1[0]-p2[0]) <= 1 and abs(p1[1]-p2[1]) <= 1 


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":


    # Ler o ficheiro de input de sys.argv[1],
    myBoard = Board.parse_instance(sys.argv[1])
    
    # Usar uma técnica de procura para resolver a instância,
    myProblem = Numbrix(myBoard)

    # Retirar a solução a partir do nó resultante,
    objective = depth_first_tree_search(myProblem)

    # Imprimir para o standard output no formato indicado.
    print("The solution is:\n", objective.state.board, sep="")
    
