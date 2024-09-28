import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (700, 700)
BOARD_SIZE = (500, 500)
GRID_SIZE = 9
CELL_SIZE = BOARD_SIZE[0] // GRID_SIZE
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
RESET_BUTTON_COLOR = (255, 0, 0)
RESET_BUTTON_SIZE = (80, 40)

# Setup the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game")

# Font for displaying text
font = pygame.font.SysFont(None, 24)

# Function to draw the grid
def draw_grid():
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(board_surface, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, BOARD_SIZE[1]))
        pygame.draw.line(board_surface, GRID_COLOR, (0, x * CELL_SIZE), (BOARD_SIZE[0], x * CELL_SIZE))

# Function to draw the reset button
def draw_reset_button():
    reset_button_rect = pygame.Rect(WINDOW_SIZE[0] - RESET_BUTTON_SIZE[0] - 10, 10, *RESET_BUTTON_SIZE)
    pygame.draw.rect(window, RESET_BUTTON_COLOR, reset_button_rect)
    text_surface = font.render("Reset", True, (255, 255, 255))
    window.blit(text_surface, (WINDOW_SIZE[0] - RESET_BUTTON_SIZE[0] - 5, 15))
    return reset_button_rect

# Function to clear the board
def clear_board():
    global characters
    characters = []

# Function to draw character circles
def draw_characters():
    for char in characters:
        pygame.draw.circle(board_surface, char['color'], (char['x'], char['y']), CELL_SIZE // 3)

# Function to display character stats
def draw_character_stats():
    y_offset = 20
    for char in characters:
        text_surface = font.render(f"Character: Color {char['color']}, Pos ({char['grid_x']}, {char['grid_y']})", True, (0, 0, 0))
        window.blit(text_surface, (20, y_offset))
        y_offset += 20

# Create a surface for the board
board_surface = pygame.Surface(BOARD_SIZE)
board_rect = board_surface.get_rect()
board_rect.topleft = (WINDOW_SIZE[0] - BOARD_SIZE[0], 0)

# Initialize characters on the board
characters = []

# Main game loop
running = True
while running:
    window.fill(BACKGROUND_COLOR)
    board_surface.fill((255, 255, 255))
    
    # Draw the grid on the board surface
    draw_grid()
    
    # Draw characters on the grid
    draw_characters()
    
    # Draw the reset button
    reset_button_rect = draw_reset_button()

    # Draw character stats on the left side
    draw_character_stats()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check if reset button is pressed
            if reset_button_rect.collidepoint(mouse_pos):
                clear_board()
            else:
                # Place a new character on the board
                if board_rect.collidepoint(mouse_pos):
                    grid_x = (mouse_pos[0] - board_rect.left) // CELL_SIZE
                    grid_y = mouse_pos[1] // CELL_SIZE
                    char_x = board_rect.left + grid_x * CELL_SIZE + CELL_SIZE // 2
                    char_y = grid_y * CELL_SIZE + CELL_SIZE // 2
                    characters.append({'color': (0, 0, 255), 'x': char_x, 'y': char_y, 'grid_x': grid_x, 'grid_y': grid_y})

    # Draw the board surface onto the main window
    window.blit(board_surface, board_rect.topleft)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
