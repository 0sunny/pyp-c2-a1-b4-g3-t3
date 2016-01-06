"""File which implements the battleship game."""

import random
import string

class Board(object):
    """Class definition for Board as a lazy representation."""
    
    def __init__(self, height = 10, width = 10):
        """Create a board with the given height and width."""
        self.row_min = str(1)
        self.column_min = "A"
        self.row_max = str(height)
        self.column_max = chr(width + 64)
        self.filled_positions = set()
        self.shots_fired = set()
        self.last_shot = None
        #self.attack_shots = 10
        self.defender_says = None
    """    
    def is_game_over(self):
        filled_undamaged_positions = self.filled_positions - self.shots_fired
        if len(filled_undamaged_positions) == 0 and \
        len(self.filled_positions) > 0:
            return True
        if len(self.shots_fired) >= self.attack_shots:
            #Game lost by attacker
            return True
        return False
    """    
    def display(self, player):
        """Display the board on the console."""
        #raise NotImplementedError
        print "_", 
        print " ".join([chr(i) for i in xrange(ord(self.column_min), ord(self.column_max) + 1)])
        for j in xrange(int(self.row_min), int(self.row_max) + 1):
            print str(j) ,
            for k in (chr(i) for i in xrange(ord(self.column_min), 
            ord(self.column_max) + 1)):
                position = k + str(j)
                if player.player_mode == "A":
                    if position in self.shots_fired:
                        if position in self.filled_positions:
                            print "@" ,
                        else:
                            print "O" ,
                    else:
                        print "_" , 
                else:
                    #Check if its one of filled positions
                    if position in self.filled_positions:
                        print "x" ,
                    else:
                        print "_" ,
            print "\n"


class Player(object):
    """The player class to be inherited by the human and computer."""
    
    def __init__(self, mode):
        """Initialize the player with the given mode. mode can be A or D."""
        if mode == "A" or "D":
            self.player_mode = mode
        else:
            print "Give the player Mode"

    def position_the_board(self, board):
        """The player positions the given board."""
        raise NotImplementedError
        
    def fire_the_missile(self, board):
        """Fire the missile on the corresponding position. The position is of 
        the form A9 ..etc"""
        raise NotImplementedError
    
    def valid_missile_position(self, position, board):
        """Fire the missile on the corresponding position. The position is of 
        the form A9 ..etc"""
        try:
            #Check if position can be parsed
            int(position[1:])
            assert position[0] in string.ascii_uppercase
        except:
            return False
        if self.player_mode == "D":
            print "Currently In Defense Mode."
            raise ValueError
            return False
        #Check if position is valid to fire, already fired or out of board.
        if position in board.shots_fired:
            print "Already fired on this position."
            return False
        elif not (int(board.row_min) <= int(position[1:]) <= int(board.row_max) and  \
        board.column_min <= position[0] <= board.column_max):
            print "Position Out of board"
            return False
        else:
            return True
    
    def move(self, board):
        """Call the required move based on mode the player is in."""
        if self.player_mode == "A":
            self.fire_the_missile(board)
        else:
            #In Defend mode
            if len(board.shots_fired) > 0:
                #Game already started
                if board.last_shot in board.filled_positions:
                    print "Hit"
                else:
                    print "Miss"
            else:
                #Setup the board
                self.position_the_board(board)
    
    def valid_move(self, position, alignment, size, board):
        """Check if the move is valid or not when positioning the board."""
        #Checks for 2 conditions -- out of board and already filled
        #get the points in the vessel if positioned.
        if alignment not in ['H','V']:
            print "Alignment not valid, please use H or V"
            return False
        if alignment == "H":
            end_position = chr(ord(position[0]) + size - 1) + position[1:]
            range_positions = [chr(ord(position[0]) + i) + position[1:] 
            for i in xrange(0, size)]
        else:
            #Alignment is vertical
            end_position = position[0] + str(int(position[1:]) + size - 1)
            range_positions = [position[0] + str(int(position[1:]) + i) 
            for i in xrange(0, size)]
        #print range_positions
        #print end_position
        #Check if position or end_position is out of board
        if not \
        (int(board.row_min) <= int(position[1:]) <= int(board.row_max) and \
        board.column_min <= position[0] <= board.column_max and\
        int(board.row_min) <= int(end_position[1:]) <= int(board.row_max) and  \
        board.column_min <= end_position[0] <= board.column_max):
            print "Position out of board"
            return False
        #Check if any point filled in range of points
        if len([position for position in range_positions if position in 
        board.filled_positions]) > 0:
            print "Colliding with some other shape, select other location."
            return False
        else:
            print "valid move."
            return True
            
class Human(Player):
    """The human player class"""
    
    def move(self, board):
        """Call the required move based on mode the player is in."""
        if self.player_mode == "A":
            self.fire_the_missile(board)
        else:
            #In Defend mode
            if len(board.shots_fired) > 0:
                #Game already started
                while True:
                    try:
                        inp = raw_input("Enter if a hit or miss: ")
                        if inp in ["hit", "miss"]:
                            board.defender_says = inp
                            break
                    except KeyboardInterrupt:
                        print "Enter a valid value: either 'hit' or 'miss'."
                #Leaving the below hit or miss for verification.        
                if board.last_shot in board.filled_positions:
                    print "Hit"
                else:
                    print "Miss"
            else:
                #Setup the board
                self.position_the_board(board)
                
    def fire_the_missile(self, board):
        while True:
            position = raw_input("Select a firing position: ")
            if self.valid_missile_position(position, board):
                board.shots_fired.add(position)
                board.last_shot = position
                print "The attacker fired at {} position".format(position)
                break
            else:
                print "Please input a valid position"
   
    def position_the_board(self, board):
        for boat_size in [3, 5, 2, 2]:
            while True:
                pos_align = raw_input("Select position and alignment for boat of size {} (e.g C9-H, A5-V): ".format(boat_size))
                position, alignment = pos_align.split('-')
                if self.valid_move(position,alignment,boat_size,board):
                    if alignment == "H":
                        range_positions = [(chr(ord(position[0]) + i) +
                        "".join(position[1:])) for i in xrange(0, boat_size)]
                    else:
                        #Alignment is vertical
                        range_positions = [(position[0] + \
                        str(int("".join(position[1:])) + i)) for i in 
                        xrange(0, boat_size)]
                    board.filled_positions.update(set(range_positions))
                    break
                else:
                    print "Position and alignment is not valid."
                    
class Computer(Player):
    """"The computer player class"""
    
    def move(self, board):
        """Call the required move based on mode the player is in."""
        if self.player_mode == "A":
            if len(board.shots_fired) > 0:
                if not self.validate_defender_says(board):
                    print "Cheater!! The computer knows when it hits a mere human!!"
            self.fire_the_missile(board)
        else:
            #In Defend mode
            if len(board.shots_fired) > 0:
                #Game already started
                if board.last_shot in board.filled_positions:
                    print "Hit"
                else:
                    print "Miss"
            else:
                #Setup the board
                self.position_the_board(board)

    def validate_defender_says(self, board):
        """validates whether the defender mentioned the correct hit/miss."""
        if board.last_shot in board.filled_positions:
            return board.defender_says == 'hit'
        else:
            return board.defender_says == 'miss'

    def fire_the_missile(self, board):
        """Have the computer fire the missiles randomly."""
        while True:
            letters = [chr(i) for i in xrange(ord(board.column_min),
            ord(board.column_max))]
            letter = random.choice(letters)
            number = str(random.randint(int(board.row_min), int(board.row_max)))
            position = letter + number
            if self.valid_missile_position(position, board):
                board.shots_fired.add(position)
                board.last_shot = position
                print "The attacker fired at {} position".format(position)
                break
            
    def position_the_board(self, board):
        """Have the computer position the board randomly."""
        for boat_size in [3, 5, 2, 2]:
            while True:
                letters = [chr(i) for i in xrange(ord(board.column_min),
                ord(board.column_max))]
                letter = random.choice(letters)
                number = str(random.randint(int(board.row_min), int(board.row_max)))
                position = letter + number
                alignment = random.choice(['H', 'V'])
                if self.valid_move(position,alignment,boat_size,board):
                    if alignment == "H":
                        range_positions = [chr(ord(position[0]) + i) +
                        position[1] for i in xrange(0, boat_size)]
                    else:
                        #Alignment is vertical
                        range_positions = [position[0] + str(int(position[1]) +
                        i) for i in xrange(0, boat_size)]
                    board.filled_positions.update(set(range_positions))
                    break
                

class GameEngine(object):
    """Implements the game logic."""
    
    def __init__(self, max_shots = 10):
        """Initialize the game."""
        self.board = Board()
        modes = ["A", "D"]
        random.shuffle(modes)
        self.human = Human(modes[0])
        self.computer = Computer(modes[1])
        self.attack_shots = max_shots
        
    def is_game_over(self):
        filled_undamaged_positions = self.board.filled_positions - self.board.shots_fired
        if len(filled_undamaged_positions) == 0 and \
        len(self.board.filled_positions) > 0:
            return True
        if len(self.board.shots_fired) >= self.attack_shots:
            #Game lost by attacker
            return True
        return False

    def run(self):
        """Start the game and run it completion."""
        print "Player is in {} mode".format(self.human.player_mode)
        
        #Start playing
        while not self.is_game_over():
            if self.human.player_mode == "D":
                self.human.move(self.board)
                print "Displaying the board, for the next shot"
                self.board.display(self.human)
                self.computer.move(self.board)
            else:
                self.computer.move(self.board)
                print "Displaying the board, for the next shot"
                self.board.display(self.human)
                self.human.move(self.board)
        #Call the diplay board and player move after the 10 shots of attacker are done.
        self.board.display(self.human)
        self.computer.move(self.board)
        self.metrics()
    
    def metrics(self):
        """Calculate the metrics."""
        filled_undamaged_positions = self.board.filled_positions - self.board.shots_fired
        if len(filled_undamaged_positions) > 0:
            print "The attacker lost the game."        
        print "Number of shots taken to complete the game : {}".format(len(self.board.shots_fired))
        print "Number of hits at the end of the game : {}".format(len(self.board.filled_positions & self.board.shots_fired))
        print "Accuracy of the attacker is {}".format(1.0*len(self.board.filled_positions & self.board.shots_fired)/len(self.board.shots_fired))


if __name__ == "__main__":
    """Run the game."""
    
    game = GameEngine()
    game.run()