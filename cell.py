class Cell:
    def __init__(self, contains_bomb=False, neighbors=0, is_revealed=False, is_flagged=False):
        self.contains_bomb = contains_bomb
        self.neighbors = neighbors
        self.is_revealed = is_revealed
        self.is_flagged = is_flagged

    def reveal(self):
        """
        Reveals the cell.
        :return: True if the cell contains a bomb, False otherwise.
        """
        self.is_revealed = True
        return self.contains_bomb

    def toggle_flag(self):
        """Toggles the flag status of the cell."""
        self.is_flagged = not self.is_flagged
      
