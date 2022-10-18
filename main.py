import pygame
import numpy as np
import time

# Start screen with height and width
pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# Fill with a background color
bg = 25, 25, 25
screen.fill(bg)

# Define game cells
nxC, nyC = 25, 25

# Width and height of each cell
dimCw = width / nxC
dimCh = height / nyC

# Matrix with states cells
# 1: Living cell
# 0: Dead cell
gameState = np.zeros((nxC, nyC))

# Examples of automata 1 (stick)
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Examples of automata 2 (movement)
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Execution control
pauseExecute = False

# Infinite loop for execution
while True:
    # For each interaction save a copy of game
    newGameState = np.copy(gameState)

    # Refresh screen with background
    screen.fill(bg)

    # Sleep system
    time.sleep(0.1)

    # Log keyboard and mouse events
    ev = pygame.event.get()

    # Events
    for event in ev:
        # If a key is pressed it pauses
        if event.type == pygame.KEYDOWN:
            pauseExecute = not pauseExecute

        # Detect if a mouse button is pressed
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            # Get position click mouse
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCw)), int(np.floor(posY / dimCh)),
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExecute:
                # Calculate number of nearest neighbors
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[x % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, y % nyC] + \
                          gameState[(x + 1) % nxC, y % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[x % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: A cell with exactly 3 living neighbors "revives"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1  # 1 living cell

                # Rule 2: A cell with less than 2 or more than 3 living neighbor cells "dies"
                if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0  # 0 dead cell

                # Create polygon of each cell to draw
                poly = [(x * dimCw, y * dimCh),
                        ((x + 1) * dimCw, y * dimCh),
                        ((x + 1) * dimCw, (y + 1) * dimCh),
                        (x * dimCw, (y + 1) * dimCh)]

                # Draw polygon (screen, colorRGB, polygon, border )
                # Depending on whether the cell is alive or dead
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Update state of game
    gameState = np.copy(newGameState)

    # gameState = np.copy(newGameState)
    pygame.display.flip()
