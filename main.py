import random

class Minesweeper:

    BOMB_RATE = 0
    SIZE = 0
    BOARD = None
    DISPLAY = None
    REVEALED = 0
    DIRS = [[-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0]]

    def __init__(self, size=5, bomb_rate=0.1):
        self.BOARD = [[0] * size for i in range(0, size)]
        self.DISPLAY = [['O'] * size for i in range(0, size)]
        self.SIZE = size
        self.BOMB_RATE = bomb_rate

        # select x random places for bombs
        # at each bomb, update bomb count in adjacent spaces
        bombs = random.sample([i for i in range(0, size*size)], int(self.BOMB_RATE*size*size))
        for b in bombs:
            r = b // size
            c = b % size
            self.BOARD[r][c] = -1
            
            for d in self.DIRS:
                new_r = r+d[0]
                new_c = c+d[1]
                if(new_r < 0 or new_r >= self.SIZE or new_c < 0 or new_c >= self.SIZE):
                    continue
                
                if(self.BOARD[new_r][new_c] != -1):
                    self.BOARD[new_r][new_c] += 1

    def print_display(self):
        print(f'+{'-' * (2 * size + 1)}+')
        print(f'| {' '.join([str(i) for i in range(0, self.SIZE)])} |')
        print(f'+{'-' * (2 * size + 1)}+---+')
        for i, row in enumerate(self.DISPLAY):
            print(f'| {' '.join(row)} | {i} |')
        print(f'+{'-' * (2 * size + 1)}+---+')
    
    def print_board(self):
        print(f'+{'-' * (2 * size + 1)}+')
        print(f'| {' '.join([str(i) for i in range(0, self.SIZE)])} |')
        print(f'+{'-' * (2 * size + 1)}+---+')
        for i, row in enumerate(self.BOARD):
            # can this be done more succintly?
            line = '| '
            for num in row:
                c = num
                if(num == 0):
                    c = 'X'
                elif(num == -1):
                    c = 'B'
                line += f'{c} '
            line += f'| {i} |'
            print(line)
        print(f'+{'-' * (2 * size + 1)}+---+')
    
    def recursive_reveal(self, r, c):
        if(r < 0 or r >= self.SIZE or c < 0 or c >= self.SIZE or self.DISPLAY[r][c] != 'O'):
            return
        
        if(self.BOARD[r][c] != 0):
            self.DISPLAY[r][c] = str(self.BOARD[r][c])
            self.REVEALED += 1
            return

        self.DISPLAY[r][c] = 'X'
        self.REVEALED += 1
        for d in self.DIRS:
            self.recursive_reveal(r+d[0], c+d[1])

    def reveal(self, c, r) -> int:
        if(r < 0 or r >= self.SIZE or c < 0 or c >= self.SIZE or self.DISPLAY[r][c] == 'X'):
            print('invalid move')
            return 0
        elif(self.DISPLAY[r][c] == 'F'):
            print('you can\'t reveal a flagged space')
            return 0
        elif(self.BOARD[r][c] == -1):
            print('lmao fail')
            self.print_board()
            return 1

        self.recursive_reveal(r, c)
        if(self.REVEALED + int(self.BOMB_RATE*self.SIZE*self.SIZE) == self.SIZE*self.SIZE):
            print('you win!!!!!')
            self.print_board()
            return 2
        
        return 0
    
    def flag(self, c, r):
        if(r < 0 or r >= self.SIZE or c < 0 or c >= self.SIZE):
            print('invalid move')
            return
        elif(self.DISPLAY[r][c] == 'F'):
            self.DISPLAY[r][c] = 'O'
            return
        elif(self.DISPLAY[r][c] != 'O'):
            print('you can\'t flag a revealed space')
            return
        

        self.DISPLAY[r][c] = 'F'

size = input('enter board size: ')
try:
    size = int(size)
except:
    print('invalid board size')
    exit()

ms = Minesweeper(size)
ms.print_display()

while(True):
    com = input('enter move: ')
    args = com.split(' ')

    if(args[0] == 'r'):
        code = ms.reveal(int(args[1]), int(args[2]))
        if(code != 0):
            exit()
    elif(args[0] == 'f'):
        ms.flag(int(args[1]), int(args[2]))
    elif(args[0] == 'q'):
        exit()
    else:
        print('invalid argument')
    
    ms.print_display()