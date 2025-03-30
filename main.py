from interface import GameInterface

if __name__ == "__main__":
    size = 6  # Taille de la grille
    num_bombs = 10  # Nombre de bombes
    game_interface = GameInterface(size, num_bombs)
    game_interface.run()
