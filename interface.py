import pygame
from game import Game

class GameInterface:
    def __init__(self, size, num_bombs):
        self.game = Game(size, num_bombs)  # Logique du jeu
        self.cell_size = 40  # Taille des cellules en pixels
        self.screen = None
        self.running = True

    def init_pygame(self):
        """Initialise Pygame et la fenêtre."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.game.grid.size * self.cell_size, self.game.grid.size * self.cell_size))
        pygame.display.set_caption("Démineur")

    def draw_grid(self):
        """Dessine la grille selon l'état actuel."""
        for i in range(self.game.grid.size):
            for j in range(self.game.grid.size):
                x, y = j * self.cell_size, i * self.cell_size
                cell = self.game.grid.grid[i][j]

                # Déterminer la couleur de la cellule
                if cell.is_revealed:
                    if cell.contains_bomb:
                        color = (255, 0, 0)  # Rouge pour les bombes
                    else:
                        color = (200, 200, 200)  # Gris clair pour les cellules révélées
                else:
                    color = (100, 100, 100)  # Gris foncé pour les cellules non révélées

                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 2)

                # Afficher le nombre de voisins si révélé
                if cell.is_revealed and not cell.contains_bomb and cell.neighbors > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(cell.neighbors), True, (0, 0, 0))
                    self.screen.blit(text, (x + 10, y + 5))

    def handle_click(self, pos):
        """Gère le clic de l'utilisateur."""
        x, y = pos
        col, row = x // self.cell_size, y // self.cell_size

        # Appelle la logique de jeu pour révéler la cellule
        result = self.game.reveal_cell(row, col)
        if result == "Game Over":
            print("💥 Vous avez perdu !")
            self.running = False
        elif result == "Victory":
            print("🎉 Félicitations, vous avez gagné !")
            self.running = False

    def run(self):
        """Boucle principale de l'interface graphique."""
        self.init_pygame()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.screen.fill((255, 255, 255))  # Fond blanc
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()
        print("Fin du jeu.")
