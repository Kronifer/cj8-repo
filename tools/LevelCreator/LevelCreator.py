import pickle
import tkinter as tk

import pygame

LevelWidth, LevelHeight = 0, 0

# Init pygame modules
pygame.init()

# Get target size of the level
root = tk.Tk()
canvas1 = tk.Canvas(root, width=200, height=150)
canvas1.pack()
entry1 = tk.Entry(root, width=2)
entry2 = tk.Entry(root, width=2)
label1 = tk.Label(root, text='size =')
label2 = tk.Label(root, text='x')

canvas1.create_window(60, 45, window=label1)
canvas1.create_window(85, 45, window=entry1)
canvas1.create_window(100, 45, window=label2)
canvas1.create_window(115, 45, window=entry2)


def setsize() -> None:
    """Sets the size of the window."""
    global LevelWidth, LevelHeight
    LevelWidth = int(entry1.get())
    LevelHeight = int(entry2.get())
    root.destroy()


button1 = tk.Button(text='Create level', command=setsize)
canvas1.create_window(100, 80, window=button1)

root.mainloop()

# Declare tile types
AIR = (0, 0, 0)
GRASS = (100, 200, 40)
LAVA = (252, 144, 3)
WATER = (0, 0, 255)
PLAYER = (100, 100, 100)
SPIKE_UP = (156, 156, 156)
SPIKE_DOWN = (51, 51, 51)

types = ['GRASS', 'LAVA', 'WATER', 'PLAYER', 'SPIKE_UP', 'SPIKE_DOWN']
colorTypes = [GRASS, LAVA, WATER, PLAYER, SPIKE_UP, SPIKE_DOWN]

# Set default type
select = 'GRASS'
colorSelect = GRASS

# Create the window
screen = pygame.display.set_mode([LevelWidth * 20, (LevelHeight * 20) + 20])
pygame.display.set_caption('Level Creator')


def savelevel(data: any, savename: str) -> None:
    """Saves the created level to the supplied filename."""
    with open(savename, 'wb') as file:
        pickle.dump(data, file)


def drawsq(color: str, pos: tuple) -> None:
    """Draws a square in the given position with the specified color."""
    pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], 20, 20))


grid = [['' for i in range(LevelWidth)] for j in range(LevelHeight)]
colorGrid = [['' for i in range(LevelWidth)] for j in range(LevelHeight)]

running = True
while running:
    for event in pygame.event.get():
        # Check to quit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos
            # Place or remove tiles on the map
            if 0 < mouse[0] < LevelWidth * 20 and 20 < mouse[1] < (LevelHeight * 20) and event.button in [1, 6]:
                grid[mouse[1] // 20][mouse[0] // 20] = select if event.button == 1 else ''
                colorGrid[mouse[1] // 20][mouse[0] // 20] = colorSelect if event.button == 1 else AIR
            # Tile selection menu
            if 0 < mouse[0] < LevelWidth * 20 and 0 < mouse[1] < 20 and event.button == 1:
                xUnit = mouse[0] // 20
                try:
                    select = types[xUnit]
                    colorSelect = colorTypes[xUnit]
                except IndexError:
                    pass
            # Export button
            if (LevelWidth - 1) * 20 < mouse[0] < LevelWidth * 20 and 0 < mouse[1] < 20 and event.button == 1:
                savelevel(grid, 'save.level')
                print('Saved "save.level"!')

    # Draw the map tiles
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if not grid[y][x] == '':
                drawsq(colorGrid[y][x], (x * 20, y * 20))

    # Draw the tile selection bar
    for i in range(len(types)):
        drawsq(colorTypes[i], (i * 20, 0))

    # Draw the yellow export button
    drawsq((252, 231, 3), ((LevelWidth - 1) * 20, 0))

    # Draw the grid
    for x in range(0, (LevelWidth * 20), 20):
        for y in range(20, 20 + (LevelHeight * 20), 20):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 20, 20), 1)

    # Draw the red bounding box
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 20, LevelWidth * 20, LevelHeight * 20), 1)

    # Update screen then wipe the buffer for the next frame
    pygame.display.flip()
    screen.fill((0, 0, 0))

pygame.quit()
