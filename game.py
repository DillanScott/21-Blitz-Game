from board import Board
import random
from time import sleep
from threading import Thread
import os

done = False
timeLeft = 180
# 3 minute timer to finish the game
def timer():
    global timeLeft
    while timeLeft > 0:
        sleep(1)
        timeLeft -= 1
        if done:
            break
    else:
        print('\n\nTimes up!')
        finishedGame()


# Check the status of the column where a card was added
def checkColumn(column):
    if column.cards[4] == ('J', 'b'):
        gameBoard.points += 200
        gameBoard.streak += 1
        column.cards = [None,None,None,None,None]
        column.total = 0
        column.acesUsed = 0

    elif column.isBust():
        gameBoard.busts += 1
        if gameBoard.streak > 0:
            gameBoard.points += (125 * (gameBoard.streak - 1) ** 2 + 125 * (gameBoard.streak - 1))
        gameBoard.streak = 0

    elif column.isFull21():
        gameBoard.points += 1000
        gameBoard.streak += 1

    elif column.is21():
        gameBoard.points += 400
        gameBoard.streak += 1

    elif column.isFull():
        gameBoard.points += 600
        gameBoard.streak += 1

    elif gameBoard.streak > 0:
        gameBoard.points += (125 * (gameBoard.streak - 1) ** 2 + 125 * (gameBoard.streak - 1))
        gameBoard.streak = 0
    else:
        pass    


# Finalises the user's score and outputs it
def finishedGame():
    global done
    done = True
    gameBoard.points += (timeLeft * 10)
    if gameBoard.streak > 0:
        gameBoard.points += (125 * (gameBoard.streak - 1) ** 2 + 125 * (gameBoard.streak - 1))
    if len(shuffledDeck) <= 0:
        if gameBoard.busts == 0:
            gameBoard.points += 100
        if gameBoard.col1 == [None,None,None,None,None] and gameBoard.col2 == [None,None,None,None,None] and gameBoard.col3 == [None,None,None,None,None] and gameBoard.col4 == [None,None,None,None,None]:
            gameBoard.points += 900
    print('\nTime left:', timeLeft)       
    print('You finished with a score of:', gameBoard.points)
    os._exit(1)

    
# Main game in a function for threading
def game():
    # Creates a deck of cards (colours only, no suits)
    colours = ['r', 'r', 'b', 'b']
    deck = []
    
    for colour in colours:
        deck.append(('A', colour))   
        
        for value in range(2, 11):
            deck.append((value,colour))
        
        deck.append(('J', colour))
        deck.append(('Q', colour))
        deck.append(('K', colour))

    
    # Shuffles the deck of cards
    global shuffledDeck
    shuffledDeck = deck
    random.shuffle(shuffledDeck)

    # Instantiates the Board class, outputs it for the 1st time and starts the 3min timer
    global gameBoard
    gameBoard = Board()
    gameBoard.output()

    # Main game loop, continues until players:
    # busts 3 time or plays through the whole deck
    while gameBoard.busts < 3 and len(shuffledDeck) > 0:
        
        topCard = shuffledDeck[0]
        print(topCard)

        # Asks where to place the top card and removes it from deck
        chosenColumn = int(input('\nWhich column would you like to add this card to?'))        
        if chosenColumn == 1:
            gameBoard.col1.addCard(topCard)
            checkColumn(gameBoard.col1)

        if chosenColumn == 2:
            gameBoard.col2.addCard(topCard)
            checkColumn(gameBoard.col2)

        if chosenColumn == 3:
            gameBoard.col3.addCard(topCard)
            checkColumn(gameBoard.col3)

        if chosenColumn == 4:
            gameBoard.col4.addCard(topCard)
            checkColumn(gameBoard.col4)
        

        shuffledDeck.pop(0)

        if timeLeft == 0:
            break

        os.system('cls' if os.name == 'nt' else 'clear')
        gameBoard.output()

    else:
        finishedGame()



if __name__ =='__main__':
    # Creates 2 threads to run alonside each other
    # Timer thread to run in background
    t1 = Thread(target=timer)
    # Game thread to run the actual game
    t2 = Thread(target=game)

    t1.start()
    t2.start()