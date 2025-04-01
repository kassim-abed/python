import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 600, 700  # Height increased to accommodate the Quit button

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Difficulty Levels
difficulty_levels = {
    "easy": (8, 10),   # (grid size, number of mines)
    "medium": (12, 20),
    "hard": (16, 40),
}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Game variables
grid = []
revealed = []
flags = []
question_marks = []
game_over = False
difficulty_selected = False
GRID_SIZE = 0
MINE_COUNT = 0
CELL_SIZE = 0
start_time = 0  # Timer variable

def initialize_game():
    global grid, revealed, flags, question_marks, game_over, CELL_SIZE, start_time
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    question_marks = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    start_time = pygame.time.get_ticks()  # Start the timer
    CELL_SIZE = WIDTH // GRID_SIZE

    # Place mines
    for _ in range(MINE_COUNT):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[y][x] == -1:  # Ensure no duplicate mines
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[y][x] = -1

    # Calculate numbers for neighboring mines
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == -1:
                continue
            count = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE and grid[ny][nx] == -1:
                        count += 1
            grid[y][x] = count

def draw_menu():
    screen.fill(WHITE)
    font_title = pygame.font.Font(None, 80)
    font_buttons = pygame.font.Font(None, 50)

    # Draw Title
    title_text = font_title.render("Mine Sweeper", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 100)))

    # Draw Buttons
    text_easy = font_buttons.render("Easy", True, BLACK)
    text_medium = font_buttons.render("Medium", True, BLACK)
    text_hard = font_buttons.render("Hard", True, BLACK)
    text_quit = font_buttons.render("Quit", True, BLACK)

    pygame.draw.rect(screen, GREEN, (150, 200, 300, 50))
    pygame.draw.rect(screen, BLUE, (150, 300, 300, 50))
    pygame.draw.rect(screen, RED, (150, 400, 300, 50))
    pygame.draw.rect(screen, YELLOW, (150, 500, 300, 50))
    
    screen.blit(text_easy, text_easy.get_rect(center=(WIDTH // 2, 225)))
    screen.blit(text_medium, text_medium.get_rect(center=(WIDTH // 2, 325)))
    screen.blit(text_hard, text_hard.get_rect(center=(WIDTH // 2, 425)))
    screen.blit(text_quit, text_quit.get_rect(center=(WIDTH // 2, 525)))
    
    pygame.display.flip()

# Game loop
running = True
double_click_timer = 0  # Timer for detecting double right-click
while running:
    if not difficulty_selected:
        draw_menu()
    else:
        screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if not difficulty_selected:
                if 150 <= mx <= 450:  # Buttons are horizontally aligned
                    if 200 <= my <= 250:  # Easy button
                        GRID_SIZE, MINE_COUNT = difficulty_levels["easy"]
                        difficulty_selected = True
                        initialize_game()
                    elif 300 <= my <= 350:  # Medium button
                        GRID_SIZE, MINE_COUNT = difficulty_levels["medium"]
                        difficulty_selected = True
                        initialize_game()
                    elif 400 <= my <= 450:  # Hard button
                        GRID_SIZE, MINE_COUNT = difficulty_levels["hard"]
                        difficulty_selected = True
                        initialize_game()
                    elif 500 <= my <= 550:  # Quit button
                        running = False
            elif game_over:  # Restart game on click after game over
                difficulty_selected = False
            else:
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Ensure within grid
                    if event.button == 1:  # Left click to reveal
                        if not revealed[y][x] and not flags[y][x] and not question_marks[y][x]:
                            revealed[y][x] = True
                            if grid[y][x] == -1:  # Mine clicked
                                game_over = True
                    elif event.button == 3:  # Right click for flags or double click for ?
                        current_time = pygame.time.get_ticks()
                        if current_time - double_click_timer <= 300:  # Double click detected
                            if not revealed[y][x] and not flags[y][x]:
                                question_marks[y][x] = not question_marks[y][x]
                        else:  # Single click for flag
                            if not revealed[y][x] and not question_marks[y][x]:
                                flags[y][x] = not flags[y][x]
                        double_click_timer = current_time

    if difficulty_selected:
        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if revealed[y][x]:
                    pygame.draw.rect(screen, GRAY, rect)
                    if grid[y][x] == -1:
                        pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                    elif grid[y][x] > 0:
                        font = pygame.font.Font(None, CELL_SIZE // 2)
                        text = font.render(str(grid[y][x]), True, BLACK)
                        screen.blit(text, text.get_rect(center=rect.center))
                elif flags[y][x]:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE // 4)
                elif question_marks[y][x]:
                    pygame.draw.rect(screen, GRAY, rect)
                    font = pygame.font.Font(None, CELL_SIZE // 2)
                    text = font.render("?", True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Display Timer
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
        font = pygame.font.Font(None, 50)
        timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        screen.blit(timer_text, (10, 10))  # Display timer in the top-left corner

        # Display Game Over screen
        if game_over:
            font = pygame.font.Font(None, 80)
            text = font.render("GAME OVER", True, RED)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()

pygame.quit()
