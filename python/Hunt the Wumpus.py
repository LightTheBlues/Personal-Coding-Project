import random
import pathlib
import re
import os


# ---------------------------------------------------------
# Create a Score File if it doesn't exist
def scoreFile():
    """
    A file name htwDataFile should be created
    Only Data it store the the points
    Only create if there is a Documents directry.
    Work on Window, Mac and Linux unsure.
    """
    fileName = "htwDataFile"
    userHome = pathlib.Path.home()
    sourceDirectory = userHome / "Documents"
    sourceFilePath = sourceDirectory / fileName

    #make only if it doesn't exist
    sourceDirectory.mkdir(parents=True, exist_ok=True)

    # Create the score file if it doesn't exist
    if not os.path.exists(sourceFilePath):
        with open(sourceFilePath, "w") as file:
            file.write('0\n')

# ---------------------------------------------------------
# Read a Score File if it exist, else return 0
def readScoreFile():
    """
    Open the file read the data from it, since there is only one data under this file so I don't have to worry about it.
    Return 0 if file not found or it's not a int
    """
    fileName = "htwDataFile"
    userHome = pathlib.Path.home()
    sourceDirectory = userHome / "Documents"
    sourceFilePath = sourceDirectory / fileName
    try:
        with open(sourceFilePath, 'r') as file:
            return int(file.readline())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0
    else:
        return score

# ---------------------------------------------------------
# Save to a Score file
def saveToScoreFile(score):
    """
    this code should work if the previous code happened
    It write the score back to the file.
    """
    fileName = "htwDataFile"
    userHome = pathlib.Path.home()
    sourceDirectory = userHome / "Documents"
    sourceFilePath = sourceDirectory / fileName

    with open(sourceFilePath, 'w') as file:
        file.write(str(score) + '\n')

# ---------------------------------------------------------------------------------------------------
# Create a random map
def createMap(size):
    # to generate a row and column using random.randint(0, size - 1)
    wumpus = (random.randint(0, size - 1), random.randint(0, size - 1))

    gold = (random.randint(0, size - 1), random.randint(0, size - 1))

    """
    since there is many pits, I like to generate the pit in a list, it random amount of pit using random.randint()
    the tuple list look like pit = [(x1, y1), (x2, y2), (x3, y3)]
    then make sure there is no pit already
    then make sure the pit isn't at the spawn
    """
    numPits = random.randint(size - 1, (size * 2) - 2)
    pit = []
    for pits in range(numPits):
        column = random.randint(0, size - 1)
        row = random.randint(0, size - 1)
        while (
            column,
            row,
        ) in pit:  # check if there is an pit already, if yes, generate a new postion
            column = random.randint(0, size - 1)
            row = random.randint(0, size - 1)

        while (column, row) == (0, 0):  # no pit at the starting postion
            column = random.randint(0, size - 1)
            row = random.randint(0, size - 1)
        pit.append((column, row))

    return wumpus, pit, gold


# ---------------------------------------------------------------------------------------------------
# Draw the game map
def drawMap(size, player_position, wumpus, pit, gold, discovered):
    print("\n")
    for row in reversed(range(size)):

        print("\t\t \t \t", end=" ")  # make it more middle of the screen

        for col in range(size):

            position = (row, col)

            if position == player_position:
                print("P", end=" ")  # Player
            elif position == wumpus:
                print("X", end=" ")  # Wumpus
            elif position in pit:
                print("X", end=" ")  # Pit
            elif position == gold:
                print("X", end=" ")  # Gold
            # after player disover a (column,row) space it's safe (the game didn't end), draw it as '-' instead
            elif position in discovered:  # Empty
                print("-", end=" ")
            else:
                print("X", end=" ")  # not discover
        print()
    print("\n")


# ---------------------------------------------------------------------------------------------------
# Draw the game map
def drawDieMap(size, player_position, wumpus, pit, gold):
    # same strategies as drawMap, but this time the game ended already so just draw the map
    print("\n")
    print("There is the map you explore")
    print()
    for row in reversed(range(size)):

        print("\t\t", end=" ")  # make it more middle of the screen

        for col in range(size):

            position = (row, col)
            if position == wumpus:
                print("W", end=" ")  # Wumpus
            elif position in pit:
                print("P", end=" ")  # Pit
            elif position == gold:
                print("G", end=" ")  # Gold
            else:
                print("-", end=" ") #empty
        print()

    print("\n")
    print("w stand for Wumpus")
    print("P stand for Pit")
    print("G stand for Gold")
    print("Note if you don't see the G, it is impossible for you to reach to the gold")

    print("\n")



# ---------------------------------------------------------------------------------------------------
# need to implment action and arrow and pick up
def action(move, player_position, size, discovered, gold, foundGold, arrow, wumpus, Score, wumpusAlive):
    """
    take player action to the game, act according
    since move in .upper in we dont have to check lowercase1234

    [0] is the row, [1] is the column
    using if statment to check if the player still in boundaries
    after checking, set that as the new postion and return it
    also add that to the discover dictionary.
    """
    valid_moves = ["W", "A", "S", "D", "F", "P"]

    if move in valid_moves:
        if move == "W":
            # Move up
            new_position = (player_position[0] + 1, player_position[1])
            if new_position[0] < size:
                player_position = new_position
                discovered.add(player_position)
        elif move == "A":
            # Move left
            new_position = (player_position[0], player_position[1] - 1)
            if new_position[1] >= 0:
                player_position = new_position
                discovered.add(player_position)
        elif move == "S":
            # Move down
            new_position = (player_position[0] - 1, player_position[1])
            if new_position[0] >= 0:
                player_position = new_position
                discovered.add(player_position)
        elif move == "D":
            # Move right
            new_position = (player_position[0], player_position[1] + 1)
            if new_position[1] < size:
                player_position = new_position
                discovered.add(player_position)
        elif move == "F":
            if arrow:
                direction = input("Enter the direction to fire (W/A/S/D): ").upper()
                if fire(direction, player_position, wumpus):
                    print("You killed the Wumpus!")
                    wumpusAlive = False
                    #wumpus = None  # Remove the Wumpus from the map
                else:
                    print("You missed the Wumpus!")
                arrow = False  # Set arrow to False after firing
            else:
                print("You don't have any arrows left!")
        elif move == "P":
            # Pick up gold, if the player picks it up, return True, and main can determine the player wins
            if player_position == gold:
                foundGold = True
                print("You picked up the gold! You win!")
    else:
        print("Invalid move. Please enter W, A, S, D, F, or P.")

    return player_position, foundGold, arrow, Score, wumpusAlive

#----------------------------------------------------------
# hit a wumpus with arrow. If the wumpus is in the same column or same row as the the shooting arrow, then it's hit, remove the wumpus from the game
def fire(direction, player_position, wumpus):
    """
    - direction: The direction in which to fire the arrow (W, A, S, or D).
    - player_position: Current position of the player.
    - wumpus: Position of the wumpus.
    - True if the arrow hits the wumpus, False otherwise.
    """
    if direction == "W":
        if player_position[0] < wumpus[0] and player_position[1] == wumpus[1]:
            return True
    elif direction == "A":
        if player_position[1] > wumpus[1] and player_position[0] == wumpus[0]:
            return True
    elif direction == "S":
        if player_position[0] > wumpus[0] and player_position[1] == wumpus[1]:
            return True
    elif direction == "D":
        if player_position[1] < wumpus[1] and player_position[0] == wumpus[0]:
            return True
    return False

# ---------------------------------------------------------------------------------------------------
# check if player died
def CheckAlive(player_position, wumpus, pit, wumpusAlive):
    # if the player postion == wumpus or pit, the player died
    if player_position == wumpus and wumpusAlive == True :
        print("You've been eaten by the Wumpus. Game Over!")
        return True
    elif player_position in pit:
        print("You fell into a pit. Game Over!")
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------
# give the player radar to sense wumpus or pit nearby.
def detectSensation(player_position, wumpus, pit, gold, wumpusAlive):

    """
    using Manhattan distance formula, aka  | x 1 − x 2 | + | y 1 − y 2 |
    we can tell how close is the nearest wumpus or pits or gold
    give player information so player can decided or to gamble for the next move
    """

    # Check if player smells the Wumpus
    wumpusDistance = abs(player_position[0] - wumpus[0]) + abs(
        player_position[1] - wumpus[1]
    )
    if wumpusDistance <= 1 and wumpusAlive == True:
        print("\t\t You smell an stench")
    # Check if player feels the breeze from nearby pits
    for pitPos in pit:
        pitDistance = abs(player_position[0] - pitPos[0]) + abs(
            player_position[1] - pitPos[1]
        )
        if pitDistance <= 1:
            print("\t\t You feel a breeze")
    goldDistance = abs(player_position[0] - gold[0]) + abs(player_position[1] - gold[1])
    if goldDistance == 0:
        print("\t\t You found the gold in the ground")
    elif goldDistance < 1:
        print("\t\t gold is nearby")


# ---------------------------------------------------------------------------------------------------
def main():
    print("\t\t Welcome to Hunt the Wumpus!\n\n")

    print("Your goal is to find the gold in this cave, avoid dying while explore the map. ")
    print("A good strategy for this game would be use the info carefully, try to determine a possible danger position and try to avoid it. \n")

    #Input Validation
    while True:
        try:
            size = int(input("\t Enter the size of the map (4, 5, 6, etc.): \n"))
            if size < 4:
                print("\t Let's make it 4 or higher.\n")
            else:
                break  # Break out of the loop when a valid size is entered
        except ValueError:
            print("\t Hey! What you input is not a number! Now try again \n")

    #File I/O.
    scoreFile() #setup by savefile if it doesn't exist
    Score = readScoreFile()
    print(" ")
    print("\t ")
    print("\t we found you record score as " + str(Score) + " \n\n ")

    playerAlive = True
    foundGold = False
    player_position = (0, 0)  # Player starts at (0, 0)
    _map = createMap(size)
    wumpus = _map[0]
    pit = _map[1]
    gold = _map[2]
    discovered = {player_position}
    wumpusAlive = True;
    arrow = True

    #Regular Expressions
    movement_pattern = re.compile(r'[WASDFP]')
    print("\t You spawn in the wumpus world, your goal is to find the gold")
    drawMap(size, player_position, wumpus, pit, gold, discovered)
    while playerAlive:
        detectSensation(player_position, wumpus, pit, gold, wumpusAlive)
        print("\n")
        move = input(
            "Enter your move (W/A/S/D to move up/left/down/right, F to fire an arrow, P to pick up gold): "
        ).upper()
        #Check for Regular Expressions r'[WASDFP]'
        if movement_pattern.match(move):
            pass

        player_position, foundGold, arrow, Score, wumpusAlive = action(
            move, player_position, size, discovered, gold, foundGold, arrow, wumpus, Score, wumpusAlive
        )
        # player find the gold, they win
        if foundGold == True:
            Score += 1000
            saveToScoreFile(Score)
            print("You Win! You score is " + str(Score))
            drawDieMap(size, player_position, wumpus, pit, gold)
            break
        # else draw the map
        drawMap(size, player_position, wumpus, pit, gold, discovered)

        # check if player died
        dead = CheckAlive(player_position, wumpus, pit, wumpusAlive)
        # need to draw a map that show the player the map after the player died
        if dead == True:
            Score -= 100
            saveToScoreFile(Score)
            print("You lost. You score is " + str(Score))
            drawDieMap(size, player_position, wumpus, pit, gold)
            break
        print()
    """
        when the program break it lead to there, where it promot to ask the player to restart the game again
    """
    while (foundGold == True or dead == True) :
        play_again = input("Do you want to play again? Enter 'yes' or 'no' ").lower()
        if play_again == 'yes':
            foundGold = False
            dead = False
            main()
        elif play_again == 'no':
            break
        else:
            print("Invalid input. Enter 'yes' or 'no'.")



if __name__ == "__main__":
    main()
