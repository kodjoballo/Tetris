import pygame
import random

# Initialize pygame
pygame.init()

# Screen and grid setup
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),    # I
    (255, 255, 0),    # O
    (128, 0, 128),    # T
    (255, 165, 0),    # L
    (0, 0, 255),      # J
    (0, 255, 0),      # S
    (255, 0, 0),      # Z
]

# Shape definitions
SHAPES = [
    [  # I
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, -1), (1, 0), (1, 1), (1, 2)],
    ],
    [  # O
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ],
    [  # T
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)],
    ],
    [  # L
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
    [  # J
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    [  # S
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ],
    [  # Z
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)],
    ]
]


clock = pygame.time.Clock()

# Initialize game board
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Helper functions
def draw_board():
    screen.fill(BLACK)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != 0:
                pygame.draw.rect(screen, COLORS[board[r][c]-1],
                                 (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for r, c in current_shape:
        pygame.draw.rect(screen, current_color,
                         (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for x in range(COLS):
        pygame.draw.line(screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
    pygame.display.flip()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def get_new_shape():
    shape_index = random.randint(0, len(SHAPES) - 1)
    rotation = 0
    shape = SHAPES[shape_index][rotation]
    color = COLORS[shape_index]
    start_col = COLS // 2 - 2
    coords = [(r, c + start_col) for r, c in shape]
    return coords, color, shape_index, rotation

def rotate_shape(shape_index, rotation, shape_pos):
    new_rotation = (rotation + 1) % len(SHAPES[shape_index])
    new_shape = SHAPES[shape_index][new_rotation]
    origin_r, origin_c = shape_pos[0]
    origin_offset = SHAPES[shape_index][rotation][0]
    offset_r, offset_c = origin_r - origin_offset[0], origin_c - origin_offset[1]
    rotated = [(r + offset_r, c + offset_c) for r, c in new_shape]
    return rotated, new_rotation


def is_valid(shape):
    for r, c in shape:
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] != 0:
            return False
    return True

def move_shape(shape, dr, dc):
    moved = [(r + dr, c + dc) for r, c in shape]
    if is_valid(moved):
        return moved
    return shape

def lock_shape():
    for r, c in current_shape:
        board[r][c] = current_index + 1

def clear_lines():
    global board, score
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLS)
    board = new_board
    score += lines_cleared * 100

# Game variables
current_shape, current_color, current_index, current_rotation = get_new_shape()
score = 0
font = pygame.font.SysFont('Arial', 24)
fall_time = 0
fall_speed = 0.5
running = True

# Game loop
while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_shape = move_shape(current_shape, 0, -1)
            elif event.key == pygame.K_RIGHT:
                current_shape = move_shape(current_shape, 0, 1)
            elif event.key == pygame.K_DOWN:
                current_shape = move_shape(current_shape, 1, 0)
            elif event.key == pygame.K_UP:
                rotated_shape, new_rotation = rotate_shape(current_index, current_rotation, current_shape)
                if is_valid(rotated_shape):
                    current_shape = rotated_shape
                    current_rotation = new_rotation

    # Auto fall
    if fall_time / 1000 > fall_speed:
        moved = move_shape(current_shape, 1, 0)
        if moved == current_shape:
            lock_shape()
            clear_lines()
            current_shape, current_color, current_index, current_rotation = get_new_shape()

            if not is_valid(current_shape):
                print("Game Over!")
                running = False
        else:
            current_shape = moved
        fall_time = 0

    draw_board()

pygame.quit()
