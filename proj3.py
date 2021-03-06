# File:    proj3.py
# Author:  Innocent Kironji
# Date:    05/04/2017
# Section: CMSC201-22
# E-mail:  wambugu1@umbc.edu 
# Description:
#   This code will allow the user to play a modified game of minesweeper

WELCOME_MSG = "\n\t" + "This program allows you to play Minesweeper." + "\n\t" + "The object of the game is to flag every mine," + "\n\t" +  "using clues about the number of neighboring" + "\n\t" + "mines in each field. To win the game, flag" + "\n\t" + "all of the mines (and don't incorrectly flag" + "\n\t" + "any non-mine fields). Good luck!" + "\n"

BOARD_PROMPT = "Enter the file to load the board from: "
MARKER_PROMPT = "Enter 'r' to reveal the space, or " + "\n" + "enter 'f' to mark the space with a flag: "
VICTORY_MSG = "You won! Congratualtions, and good game!"
LOSS_MSG = "You detonated a mine! Game Over!"

REVEAL_MARK = "r"
FLAG_MARK = "f"

#Game board key 
FLAG = "F"
BORDER = "+"
MINE = "*"
UNKNOWN = "."
ISLAND = " "
DETONATED_MINE = "X"


# board_printer()    prints the board with row and column labels,
#                    and spaces the board out so that it looks square
# Input:             board;   the rectangular 2d gameboard to print  
# Output:            none;    prints the board in a pretty way    
def board_printer(board):
    # if board is large enough, print a "tens column" line above the rows
    if len(board[0]) - 2 >= 10:
        first_line = "\n     " + ("  ") * (10 - 1)
        for i in range(10, len(board[0])-1 ):
            first_line += str(i // 10) + " "
        print(first_line, end="")

    # create and print top numbered line (and empty line before)
    top_line = "\n     "
    # only go from 1 to len - 1, so we don't number the borders
    for i in range(1, len(board[0])-1 ):
        # only print the last digit (so 15 --> 5)
        top_line += str(i % 10) + " "
    print(top_line)

    # create the border row
    border_row = "   "
    for col in range(len(board[0])):
        border_row += board[0][col] + " "

    # print the top border row
    print(border_row)
                         
    # print all the interior rows
    for row in range(1, len(board) - 1):
        # create the row label on the left
        row_str = str(row) + " "

        # if it's a one digit number, add an extra space, so they line up
        if row < 10:
            row_str += " "

        # add the row contents to the row string, and print it out
        for col in range(len(board[row])):
            row_str += str(board[row][col]) + " "
        print(row_str)

    # print the bottom border row and an empty line
    print(border_row)
    print()


# get_board()  asks the user for what board to use and stores it as a list
# Input:       board; a list variable where the game board will be stored
# Output:      none; all this function does is updates a list
def get_board(board):

    file_name = input(BOARD_PROMPT)
    board_file = open(file_name)

    #Each line is stored as its own seperate list (within a 2D list)
    for line in board_file:
        line = line.strip()
        board.append(list(line))
    board_file.close()


# count_mines() calculates the total number of mines on the board and hides
#               all locations on game board to be displayed to user
# Input:        display; a list that stores the board with hidden locations
#               solution; a list that contains the solved game board
#               row; an int that keeps track of which row is being checked 
#               mines; an int that keep track of the number of mines
# Output:       total_mines; an int that is the total number of mines on
#                            the game board
def count_mines(display, solution, row, mines):
    
    #Recursive case
    if (row < len(solution)):
        board_line = []

        #Hides locations of mines and non-mines for the user display
        for index in solution[row]:
            if (index == BORDER):
                board_line.append(index)

            #Records the number of mines
            elif (index == MINE):
                mines += 1
                board_line.append(UNKNOWN)

            else:
                board_line.append(UNKNOWN)

        #Stores hidden locations as a list
        display.append(board_line)
        return count_mines(display, solution, row + 1, mines)

    #Base case
    else:
        total_mines = mines
        return total_mines


# reveal()  reveals empty spaces and hints around the field the user
#           specifies
# Input:    row; int, contains row value for specified field
#           column; int, contains column value for specified field
#           hints; list, contains hint and mine locations
#           board; list, contains contents of game board (that is displayed)
# Output:   is_game_over; boolean, tells the user if they detonated a mine
def reveal(row, column, hints, board, island_pos):

    is_game_over = False

    #Only runs if the space is an "empty" field
    if (board[row][column] == UNKNOWN):

        #If user detonates (reveals) a mine
        if (hints[row][column] == MINE):
            board[row][column] = DETONATED_MINE
            is_game_over = True

        #Activates recusive function that will update the game board with the island surrounding the chosen field
        elif (hints[row][column] == ISLAND):
            board[row][column] = hints[row][column]

            #Runs twice so that the first time all positions for the island are stored and the second time all hints are revealed
            for hum in range(2):
                island_checker(hints, board, island_pos, row, column, 0)
            
        #If the field is a hint, the hint is revelead on the game board
        else:
            board[row][column] = hints[row][column]

        board_printer(board)

    #Cannot reveal a flagged field
    elif (board[row][column] == FLAG):
        board_printer(board)
        print("\t", "Field", str(row) + ",", column, "must be unflagged before it can be revealed") 

    #If the space is already revealed the board remains unchanged
    else:
        board_printer(board)
        print("\t", "Field", str(row) + ",", column, "was already previously revealed")
    return is_game_over


# island_checker(): checks if the surrounding area of current field is apart of the island and reveals empty and hint fields on the game board
# Input:            hints; list, holds the board where the hints are located
#                   board; list, holds the game board
#                   island_pos; list, stores all locations that are apart of the island so that the fields around those points can also be checked
#                   row; int, row of the field currently being checked
#                   column; int, column of the field currently being checked
#                   counter; int, keeps track of which field in island_pos we are currently checking
# Output:           none; this code only updates the lists for island positions and the game board
def island_checker(hints, board, island_pos, row, column, counter):

    #Defining some variables
    row_index = [-1, -1, 1, 1, -1, 1, 0, 0]
    col_index = [-1, 1, -1, 1, 0, 0, -1, 1]

    #Helps to check the points diagonal, above, below, and adjacent (left/right) of the current position
    for num in range(len(row_index)):

        #Only runs if points around the current field are not mines or borders. Also will only run if current field is empty (will not run over a hint)
        if (hints[row + row_index[num]][column + col_index[num]] != MINE) and (hints[row + row_index[num]][column + col_index[num]] != BORDER) and (hints[row + row_index[num]][column + col_index[num]] != MINE) and (board[row + row_index[num]][column + col_index[num]] == UNKNOWN) and (board[row][column] == ISLAND):

            #Saves the current space and updates the game board
            board[row + row_index[num]][column + col_index[num]] = hints[row + row_index[num]][column + col_index[num]]
            island_pos.append([row + row_index[num],column + col_index[num]])

    #Recursive case
    if(counter < len(island_pos)):
        island_checker(hints, board, island_pos, island_pos[counter][0], island_pos[counter][1], counter + 1)


# flag()   Places flag in empty spaces that have been uncovered. Removes
#          flag if already placed. Nothing happens if the field is revealed
# Input:   row; int, the row position of the user indicated field
#          column; int, the column position of the user indicated field
#          solution; a list, that contains the solution board
#          board; a list, that contains the game board
#          flags; int, the number of flags the user has remaining
# Output:  updated_flags; int, an updated number of flags the user has
def flag(row, column, solution, board, flags):

    #Places a flag
    if (board[row][column] == UNKNOWN):
        board[row][column] = FLAG
        updated_flags = flags - 1
        board_printer(board)

    #Removes flag (if there is already a flag)
    elif (board[row][column] == FLAG):
        board[row][column] = UNKNOWN
        board_printer(board)
        print("\t", "Flag removed from " + str(row) + ", " + str(column))
        updated_flags = flags + 1

    #If the field is already revelead board remains unchanged
    else:
        board_printer(board)
        print("\t", "You cannot place a flag at " + str(row) + ", " + str(column))
        updated_flags = flags

    #Show the user the updated board and flags remaining
    print("\t", "There are/is", updated_flags, "mine(s) left to find.", "\n")
    return updated_flags


# get_coord()  gets the coordinates for the field the user wants to use
# Input:       board; a list that contains the game board being used
# Ouput:       row; the row position the user wants to use
#              column; the column position the user wants to use
def get_coord(board):

    #Asks the user for the row position of the field they want to use
    print("Please choose the row:")
    end_row = len(board) - 2
    row = int(input("Enter a number between 1 and " + str(end_row) + " (inclusive): "))
    row = get_valid_coord("row", row, end_row)

    #Asks the user for the column position of the field they want to use
    print("Please choose the column:")
    end_column = len(board[0]) - 2
    column = int(input("Enter a number between 1 and " + str(end_column) + " (inclusive): "))
    column = get_valid_coord("column", column, end_column)
    
    return row, column


# get_valid_coord() checks if the user entered a valid coordinate value
# Input:            position; string, tells the code what type of coordinate
#                                     is being checked
#                   coord; int, the value for the coordinate being checked
#                   end_coord; int, the last possible number for coord
# Output:           valid_coord; int, a valid coordinate defined by the user
def get_valid_coord(position, coord, end_coord):

    #Recursive case
    if (coord < 1) or (coord > end_coord):
        print("That is not a valid number for the", position)
        coord = int(input("Enter a number between 1 and " + str(end_coord) + " (inclusive): "))
        return get_valid_coord(position, coord, end_coord)

    #Base case
    else:
        valid_coord = coord
        return valid_coord


# get_valid_mark()  checks for and gets valid marker entry from user
# Input:            action; string, represents the action the user wants
# Output:           valid_action; string, holds a letter representation of a valid action 
def get_valid_mark(action):

    #Base cases
    if (action == FLAG_MARK):
        valid_action = action
        return valid_action
    elif (action == REVEAL_MARK):
        valid_action = action
        return valid_action

    #Recursive case
    else:
        print("\t", "That is not a valid action.")
        action = input(MARKER_PROMPT)
        return get_valid_mark(action)


# get_hints()  updates hint board with values on fields adjacent to a mine
#              values are based on the number of mines adjacent
# Input:       hint_board; list that will hold hint locations and values
#              mine_locations; 2D list that contains the coordinates for
#                              the location of ever mine
# Output:      none; function only updates hint_board with hints
def get_hints(hint_board, mine_locations):
    
    #Defining some variables
    row = 0
    column = 0
    max_len = len(hint_board)
    last_pos = max_len - 1
    counter = 0

    #Sets initial values for locations with hints
    while (counter < len(mine_locations)):

        #Checks adjacent spaces for all mines
        row = mine_locations[counter][0]
        column = mine_locations[counter][1]

        #Checks fields in the row above the mine (directly above & diagonal)
        if (row > 1) and (column > 1):
            if (hint_board[row - 1][column - 1] == ISLAND):
                hint_board[row - 1][column - 1] = 0

        if (row > 1):
            if (hint_board[row - 1][column] == ISLAND):
                hint_board[row - 1][column] = 0

        if (row > 1) and (column < last_pos):
            if (hint_board[row - 1][column + 1] == ISLAND):
                hint_board[row - 1][column + 1] = 0

        #Checks fields adjacent to the mine (left/right)
        if (column > 1):
            if (hint_board[row][column - 1] == ISLAND):
                hint_board[row][column - 1] = 0
        if (column < last_pos):
            if (hint_board[row][column + 1] == ISLAND):
                hint_board[row][column + 1] = 0

        #Checks fields in the row below the mine
        if (row < last_pos) and (column > 1):
            if (hint_board[row + 1][column - 1] == ISLAND):
                hint_board[row + 1][column - 1] = 0
        if (row < last_pos):
            if (hint_board[row + 1][column] == ISLAND):
                hint_board[row + 1][column] = 0
        if (row < last_pos) and (column < last_pos):
            if (hint_board[row + 1][column + 1] == ISLAND):
                hint_board[row + 1][column + 1] = 0

        counter += 1

    #Updates the hints based on the number of mines around them
    counter = 0
    while (counter < len(mine_locations)):

        row = mine_locations[counter][0]
        column = mine_locations[counter][1]

        #Updates the row above the mine
        if (row > 1) and (column > 1):
            #Ignores spaces that are mines or borders
            if (hint_board[row - 1][column - 1] != BORDER) and (hint_board[row - 1][column - 1] != MINE): 
                hint_board[row - 1][column - 1] += 1

        if (row > 1):
            #Ignoring mines & borders happens at all points
            if (hint_board[row - 1][column] != BORDER) and (hint_board[row - 1][column] != MINE):
                hint_board[row - 1][column] += 1

        if (row > 1) and (column < last_pos):
            if (hint_board[row - 1][column + 1] != BORDER) and (hint_board[row - 1][column + 1] != MINE):
                hint_board[row - 1][column + 1] += 1

        #Updates the two point adjacent (left/right) from the mine
        if (column > 1):
            if (hint_board[row][column - 1] != BORDER) and (hint_board[row][column - 1] != MINE):
                hint_board[row][column - 1] += 1

        if (column < last_pos):
            if (hint_board[row][column + 1] != BORDER) and (hint_board[row][column + 1] != MINE):
                hint_board[row][column + 1] += 1

        #Updates the points below the mine
        if (row < last_pos) and (column > 1):
            if (hint_board[row + 1][column - 1] != BORDER) and (hint_board[row + 1][column - 1] != MINE):
                hint_board[row + 1][column - 1] += 1

        if (row < last_pos):
            if (hint_board[row + 1][column] != BORDER) and (hint_board[row + 1][column] != MINE):
                hint_board[row + 1][column] += 1

        if (row < last_pos) and (column < last_pos):
            if (hint_board[row + 1][column + 1] != BORDER) and (hint_board[row + 1][column + 1] != MINE):
                hint_board[row + 1][column + 1] += 1

        counter += 1


# list_hints()  saves the coordinates of each mine and initilizes hint_board
# Input:        mine_locations; list that holds coordinate values for
#                               each mine
#               solution; list, contains solution to game board
#               row; int, keeps track of what row we are checking
#               hint_board; list, holds copy of game board with all the
#                                 hints revelead 
# Output:       none; only updates the lists mine_locations and hint_board
def list_hints(mine_locations, solution, row, hint_board):

    #Recursive case
    if (row < len(solution)):
        board_line = []
        column = 0
        while (column < len(solution[row])):

            #Saves the coordinates of every mine
            if (solution[row][column] == MINE):
                mine_locations.append([row, column])

            board_line.append(solution[row][column])
            column += 1

        #Saves the locations of the mines on the board for hints (this will be important for placing hints correctly)
        hint_board.append(board_line)
        list_hints(mine_locations, solution, row + 1, hint_board)
            

# check_flags() Checks the board to see if all the mines have been flagged
# Input:        mine_locations; 2D list, contains coordinates for every mine
#               flag_locations; 2D list, contains coordinates for all fields
#                                        that have been flagged
#               board; 2D list, contains the game board
#               row; int, keeps track of which row is being checked
#               game_over; boolean, keeps track of whether or not the game
#                                   has ended
# Output:       is_game_over; boolean, reports whether or not the player
#                                      has achieved victory
def check_flags(mine_locations, flag_locations, board, row, game_over):

    #Recursive Case
    if (row < len(board)):
        column = 0
        while (column < len(board[row])):

            #Saves the location if it is a flag
            if (board[row][column] == FLAG):
                flag_locations.append([row, column])

            column += 1

        return check_flags(mine_locations, flag_locations, board, row + 1, game_over)

    #Base case
    else:
        
        #Game ends if every mine has been flagged
        if (mine_locations == flag_locations):
            game_over = True
            print(VICTORY_MSG)

        #Otherwise game continues
        else:
            game_over = False
            

        is_game_over = game_over
        return is_game_over


def main():
    
    #Defining some variables
    solution_board = []
    game_board = []
    hint_board = []
    mine_locations = []
    game_over = False

    print(WELCOME_MSG)

    #Set initial values for the solution, hints and the number of mines
    get_board(solution_board)
    mines = count_mines(game_board, solution_board, 0, 0)

    #Creates a complete hint_board (contains all hint locations with accurate hints)
    list_hints(mine_locations, solution_board, 0, hint_board)
    get_hints(hint_board, mine_locations)

    #print the board and the starting number of flags
    board_printer(game_board)
    flags = mines
    print("\t", "There are/is", flags, "mine(s) left to find.", "\n")

    #Allows the user to keep playing until they either flag every mine
    #or detonate any mine
    while (game_over == False):

        #Get the coordinates for the field the user wants to use
        row, column = get_coord(game_board)

        #Get valid input for what action the user wants to take
        action = input(MARKER_PROMPT)
        action = get_valid_mark(action)
    
        #When the user chooses to mark a space
        if (action == FLAG_MARK):
            flags = flag(row, column, solution_board, game_board, flags)
    
        #When the user choose to reveal a space
        elif (action == REVEAL_MARK):
            island_pos = []
            game_over = reveal(row, column, hint_board, game_board, island_pos)

            #Mine is not detonated so game continues
            if (game_over == False):
                print("\t", "There are/is", flags, "mine(s) left to find.", "\n")
            #Mine is detonated and game ends
            else:
                print(LOSS_MSG, "\n")

        #Checks if all mines have been flagged correctly and no non-mines
        #have been flagged
        if (flags == 0):
            flag_locations = []
            game_over = check_flags(mine_locations, flag_locations, game_board, 0, game_over)

main()
