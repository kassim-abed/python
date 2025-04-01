import pygame
from grid import Grid
from game import Game

# Initialisation de Pygame
pygame.init()

# Paramètres de l'affichage
CELL_SIZE = 40
GRID_SIZE = 10  # Taille de la grille (modifiable)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Démineur")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialisation du jeu
game = Game(GRID_SIZE, "medium")

# Boucle de jeu
running = True
while running:
    screen.fill(WHITE)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            cell = game.grid.grid[row][col]

            if event.button == 1:  # Clic gauche
                result = game.reveal_cell(row, col)
                if result == "Game Over":
                    print("💥 Vous avez perdu !")
                    running = False
                elif result == "Victory":
                    print("🎉 Vous avez gagné !")
                    running = False

            elif event.button == 3:  # Clic droit
                if not cell.is_revealed:
                    if not cell.is_flagged and not hasattr(cell, "is_question"):
                        cell.is_flagged = True
                    elif cell.is_flagged:
                        cell.is_flagged = False
                        cell.is_question = True
                    elif hasattr(cell, "is_question") and cell.is_question:
                        cell.is_question = False

    # Affichage de la grille
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = game.grid.grid[i][j]

            if cell.is_revealed:
                color = GRAY if not cell.contains_bomb else RED
                pygame.draw.rect(screen, color, rect)
                if not cell.contains_bomb and cell.neighbors > 0:
                    font = pygame.font.Font(None, 30)
                    text = font.render(str(cell.neighbors), True, BLACK)
                    screen.blit(text, (j * CELL_SIZE + 15, i * CELL_SIZE + 10))
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                if cell.is_flagged:
                    pygame.draw.circle(screen, BLUE, rect.center, CELL_SIZE // 4)
                elif hasattr(cell, "is_question") and cell.is_question:
                    font = pygame.font.Font(None, 30)
                    text = font.render("?", True, YELLOW)
                    screen.blit(text, (j * CELL_SIZE + 15, i * CELL_SIZE + 10))

    pygame.display.flip()

pygame.quit()
