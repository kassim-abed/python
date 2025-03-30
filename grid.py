import random
from cell import Cell

class Grid:
    def __init__(self, size):
        self.size = size
        self.num_bombs = 0  # Bombs are set by difficulty
        self.grid = []
        self.create_grid()

    def create_grid(self):
        """Creates an empty grid filled with cells."""
        for i in range(self.size):
            self.grid.append([])
            for j in range(self.size):
                self.grid[i].append(Cell())

    def set_difficulty_easy(self):
        """Sets easy mode: 10% of the grid contains bombs."""
        self.num_bombs = (self.size * self.size) // 10
        self.place_bombs()
        self.calculate_neighbors()

    def set_difficulty_medium(self):
        """Sets medium mode: 20% of the grid contains bombs."""
        self.num_bombs = (self.size * self.size) // 5
        self.place_bombs()
        self.calculate_neighbors()

    def set_difficulty_hard(self):
        """Sets hard mode: 30% of the grid contains bombs."""
        self.num_bombs = (self.size * self.size) // 3
        self.place_bombs()
        self.calculate_neighbors()

    def place_bombs(self):
        """Randomly places bombs in the grid."""
        bombs_placed = 0
        while bombs_placed < self.num_bombs:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            cell = self.grid[row][col]
            if not cell.contains_bomb:
                cell.contains_bomb = True
                bombs_placed += 1

    def calculate_neighbors(self):
        """Calculates the number of neighboring bombs for each cell."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(self.size):
            for j in range(self.size):
                cell = self.grid[i][j]
                if cell.contains_bomb:
                    continue
                neighbors = 0
                for dr, dc in directions:
                    new_row, new_col = i + dr, j + dc
                    if 0 <= new_row < self.size and 0 <= new_col < self.size:
                        if self.grid[new_row][new_col].contains_bomb:
                            neighbors += 1
                cell.neighbors = neighbors

    def reveal_neighbors(self, row, col):
        """Reveals all neighboring cells recursively if they have no neighboring bombs."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                neighbor = self.grid[new_row][new_col]
                if not neighbor.is_revealed and not neighbor.contains_bomb:
                    neighbor.reveal()
                    if neighbor.neighbors == 0:
                        self.reveal_neighbors(new_row, new_col)

                #creer trois methode de difficulté facile, moyenne et difficile
                #lier avec le menu que fait abdoullah 
                #il doit faire l'interface avec 4 boutons dont les trois difficultés + quitter
