from grid import Grid

class Game:
    def __init__(self, size, difficulty):
        self.grid = Grid(size)
        self.set_difficulty(difficulty)
        self.is_game_over = False
        self.is_victory = False

    def set_difficulty(self, difficulty):
        """Sets the game's difficulty."""
        if difficulty == "easy":
            self.grid.set_difficulty_easy()
        elif difficulty == "medium":
            self.grid.set_difficulty_medium()
        elif difficulty == "hard":
            self.grid.set_difficulty_hard()
        else:
            raise ValueError("Invalid difficulty. Choose 'easy', 'medium', or 'hard'.")

    def reveal_cell(self, row, col):
        """Reveals a cell and applies game logic."""
        if row < 0 or col < 0 or row >= self.grid.size or col >= self.grid.size:
            return "Invalid move"  # Invalid coordinates
        
        cell = self.grid.grid[row][col]

        if cell.is_revealed:
            return "Already revealed"
        
        result = cell.reveal()
        if result:  # If the cell contains a bomb
            self.is_game_over = True
            return "Game Over"
        else:
            if cell.neighbors == 0:
                self.grid.reveal_neighbors(row, col)

            if self.check_victory():
                self.is_victory = True
                self.is_game_over = True
                return "Victory"
        return "Cell revealed"

    def check_victory(self):
        """Checks if all safe cells are revealed."""
        for row in self.grid.grid:
            for cell in row:
                if not cell.is_revealed and not cell.contains_bomb:
                    return False
        return True
