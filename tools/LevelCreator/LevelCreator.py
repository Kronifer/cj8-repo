import pickle

import ezTypes as ez
import pygame

LevelWidth = int(input('Please enter the width of the level: '))
LevelHeight = int(input('Please enter the height of the level: '))

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Place or remove tiles on the map
            if 0 < event.pos[0] < LevelWidth * 20 and 20 < event.pos[1] < ((LevelHeight + 1) * 20):
                if event.button in [1, 3]:
                    grid[(event.pos[1] // 20) - 1][event.pos[0] // 20] = ez.select if event.button == 1 else ''
                    colorGrid[(event.pos[1] // 20) - 1][
                        event.pos[0] // 20] = ez.colorSelect if event.button == 1 else ez.AIR
            # Tile selection menu
            if 0 < event.pos[0] < LevelWidth * 20 and 0 < event.pos[1] < 20 and event.button == 1:
                xUnit = event.pos[0] // 20
                try:
                    ez.select = ez.types[xUnit]
                    ez.colorSelect = ez.colorTypes[xUnit]
                except IndexError:
                    pass
            # Export button
            if (LevelWidth - 1) * 20 < event.pos[0] < LevelWidth * 20 and 0 < event.pos[1] < 20 and event.button == 1:
                savelevel(grid, 'save.level')
                print('Saved "save.level"!')
        if event.type == pygame.MOUSEMOTION:
            if 0 < event.pos[0] < LevelWidth * 20 and 0 < event.pos[1] < 20:
                try:
                    pygame.display.set_caption(f'Select tile type: {ez.types[event.pos[0] // 20]}')
                except IndexError:
                    if event.pos[0] // 20 == LevelWidth - 1:
                        pygame.display.set_caption('Export')
                    else:
                        pygame.display.set_caption('Level Creator')
            else:
                pygame.display.set_caption('Level Creator')
                if event.buttons[0] == 1 or event.buttons[2] == 1:
                    grid[(event.pos[1] // 20) - 1][event.pos[0] // 20] = ez.select if event.buttons[0] == 1 else ''
                    if event.buttons[0] == 1:
                        colorGrid[(event.pos[1] // 20) - 1][event.pos[0] // 20] = ez.colorSelect
                    else:
                        colorGrid[(event.pos[1] // 20) - 1][event.pos[0] // 20] = ez.AIR

    # Draw the map tiles
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if not grid[y][x] == '':
                drawsq(colorGrid[y][x], (x * 20, (y + 1) * 20))

    # Draw the tile selection bar
    for i in range(len(ez.types)):
        drawsq(ez.colorTypes[i], (i * 20, 0))

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
