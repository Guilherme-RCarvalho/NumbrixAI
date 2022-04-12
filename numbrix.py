# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 06:
# 96868 Guilherme Carvalho
# 96884 José Mateus

import sys
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
    
        
    def makeAction(self, action: (int, int,int)): #  row: int, col: int, value: int):
        """ Recebe um tuplo com: uma linha, uma coluna e um valor, e mete esse valor na posicao dada  """        
        self.board[action[0]][action[1]] = action[2]
        return

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        if row == 0:
            return (-1,self.board[row][col+1])
        if row == self.boardSize-1:
            return (self.board[row][col-1],-1)
        return (self.board[row][col-1], self.board[row][col+1])
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        
        if col == 0:
            return (-1,self.board[row+1][col])
        if col == self.boardSize-1:
            return (self.board[row-1][col],-1)
        return (self.board[row-1][col], self.board[row+1][col])
    
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
        self.possibleStates = [] # To be filled with all the states that can be reach from the current state
        
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        
        
        # vamos primeiro a cada numero colocado, ver os vizinhos e criar estados em que os vizinhos sao todos os os numeros adjacentes
        # para isto se calhar vou querer ter um dicionario de numeros ja colocados e as posicoes deles mas por enquanto nao vou fazer isso
        
        # get the dict of placed numbers THIS CAN BE OPTIMIZED (prob create a list)
        myBoard = state.board.board
        stateList = []
        

        placedValuesDict = {} 
        for row in myBoard:
            for column in row:
                for value in column:
                    if value != 0:
                        placedValuesDict[value] = [row, column]
    
        # for each placed value (in incrementing order)
        neighborOrder = [[-1,0], [1, 0], [0, -1], [0, 1]]  # order that  I will be looking at the neighbors up, down, left, right
        for value in placedValuesDict.keys().sort():
            # pegar os adjacentes para os lados e para cima
            adjacentPostions = myBoard.adjacent_vertical_numbers() + myBoard.adjacent_vertical_numbers()

            for x in range(len(neighborOrder)):

                if adjacentPostions[x] == 0 or adjacentPostions[x] != -1:
                    continue
            
                # means that I will want to create a new state (possible two) where the possition is neighborOrder[x]
                if value == 1:
                    changeNumberList = [1]
                elif value == myBoard.boardSize*myBoard.boardSize:
                    changeNumberList = [-1]
                else:
                    changeNumberList = [1, -1]
                
                for incrimentValue in changeNumberList:
                    
                    
                    myPos = [element1 - element2 for (element1, element2) in zip(placedValuesDict[x], neighborOrder[x])]
                    stateList.append(self.result(state, (myPos[0], myPos[1], value + incrimentValue)))



    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        # I will want to create a new state, not edit the old one

        # Create the newState
        boardRepresent, filledSquare = state.board.getRawBoard()
        newBoard = Board(boardRepresent, filledSquare)
        newState = NumbrixState(newBoard)

        # Update new state
        newBoard.makeAction(action)

        
        return newState

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        
            
        tens dic com todos os val:pos;
        for x in dic:
            if x->next é vizinho continua 
             end return True
             else false

        placedValuesDict = {} 
        for row in myBoard:
            for column in row:
                for value in column:
                    if value != 0:
                        placedValuesDict[value] = [row, column]

        if state.board.filledSquares == state.board.boardSize*state.board.boardSize:
            for key in range(state.board.boardSize*state.board.boardSize)-1:
                values = placedValuesDict[key]
                if key+1 in (myBoard.adjacent_vertical_numbers(values) + myBoard.adjacent_vertical_numbers(values)):
                    pass
                else:
                    return False
            return True
        return False

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
    objective = """type_search"""(myProblem)

    # Imprimir para o standard output no formato indicado.
    print("The solution is:\n", myProblem.board.to_string(), sep="")
    
