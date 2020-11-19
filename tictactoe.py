import random
possiblewins = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8],
                [3, 6, 9], [1, 5, 9], [3, 5, 7]]
tokens = ['X', 'O']

class board:
    def __init__(self, p1, p2):
        self.players = [p1, p2]
        random.shuffle(self.players)  # Random player start
        self.occupied = list()  # List of occupied slots
        self.boardtemplate = ('''
          1  |  2  |  3
        -----|-----|-----
          4  |  5  |  6
        -----|-----|-----
          7  |  8  |  9  \n''')
        self.board = self.boardtemplate

    def checkoccupied(self, move):
        if move in self.occupied:
            return True
        else:
            return False

    def updateboard(self, moves):
        '''Occupy and update board. Input: tuple of moves (player, move)'''
        for player, move in moves:
            self.board = self.board.replace(str(move), player.token)
    
    def updateoccupied(self, move):
        self.occupied.append(move)

    def possiblemoves(self):
        '''Return a list of possible moves.'''
        pos = list()
        for i in range(1,10):
            if i in self.occupied: continue
            pos.append(i)
        return pos

    def resetboard(self):
        '''Resets the board.'''
        self.board = self.boardtemplate
        self.occupied = list()
        random.shuffle(self.players)


class player:
    def __init__(self, name, chosentoken):
        self.name = name
        self.token = self.validtoken(chosentoken)
        self.score = 0
        self.moves = list()
        self.curmove = None

    def resetscore(self):
        self.score = 0

    def won(self):
        self.score += 1

    def generatemove(self, board):  # Generate move for AI
        move = None
        while move is None:
            move = random.choice(board.possiblemoves())
        return move

    def validtoken(self, token):
        global tokens
        token = token.upper()
        if token not in tokens:
            raise Exception('ERROR: Invalid token - X/O')
        else:
            return token
    
    def setmove(self, move):
        self.moves.append(move)


def checkvalidmove(move, board):
    try:
        move = int(move)  # Sanity check
    except ValueError:
        print('ERROR: Move must be an integer.', move)
        return False
    if move not in range(1, 10):
        print('ERROR: Move value must be within 1-9.')
        return False
    if board.checkoccupied(move):
        print(move, 'already occupied.')
        return False
    else:
        return True


def checkwinner(p1, p2):  # Passed arg - players
    global possiblewins
    moves_both = {p1: p1.moves, p2: p2.moves}
    for curplayer in moves_both:
        for wins in possiblewins:
            count = 0
            for mov in moves_both[curplayer]:
                if mov in wins:
                    count += 1
                if count == 3:
                    return curplayer
    return None


def compilemoves(p1, p2):
    '''Return tuple of token, move. Args: players'''
    tup = (p1, p1.curmove), (p2, p2.curmove)
    return tup


def askmoves(board):
    players = board.players
    for p in players:
        moveofplayer = None
        while moveofplayer is None:
            if p.name.startswith('AI') or p.name.startswith('ai'):
                moveofplayer = p.generatemove(board)
            else:
                moveofplayer = input('Input move (1-9): ')
            if not checkvalidmove(moveofplayer, board):
                moveofplayer = None
        p.curmove = int(moveofplayer)
        board.updateoccupied(p.curmove)


def game(player1, player2):
    p1 = player(name1, 'X')
    p2 = player(name2, 'O')
    tictactoe = board(p1, p2)
    print(f'Player {tictactoe.players[0].name} goes first!')
    print(tictactoe.board)
    winner = None
    while winner is None:
        
        askmoves(tictactoe)
        playermoves = compilemoves(p1, p2)
        for players, move in playermoves:
            players.setmove(move)
        tictactoe.updateboard(compilemoves(p1, p2))
        print(tictactoe.board)
        winner = checkwinner(p1, p2)
    print(f'Winner - {winner.name}.')
    winner.won()  # add one to winner's score
    tictactoe.resetboard()
            





if __name__ == "__main__":
    inp = None
    while True:
        
        print('Welcome to Tic-Tac-Toe!')
        print('Enter your move based on the numbers on the board.')
        # input('Press any key to play.')
        name1 = input('Enter Player 1\'s name: ')
        name2 = input('Enter Player 2\'s name: ')
        game(name1, name2)
        inp = input('Press any key to play again. \'Quit\' to quit.')
        if inp.lower() != 'quit':
            game(name1, name2)
        else: quit()



