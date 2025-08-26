Absolutely! Here's a **full walkthrough** of the Pygame Tetris code, section by section, with clear explanations so you understand how each part works and why it's there.

---

## 🎮 Tetris in Pygame – FULL CODE EXPLANATION

---

### 1. **Imports and Initialization**

```python
import pygame
import random
```

* `pygame`: used for creating the game window, drawing shapes, and handling input.
* `random`: used for selecting random Tetris shapes.

```python
pygame.init()
```

Initializes all Pygame modules. Required before using most Pygame functions.

---

### 2. **Screen and Grid Configuration**

```python
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
```

* `CELL_SIZE`: pixels per Tetris square.
* `COLS`, `ROWS`: number of columns and rows in the grid.
* `WIDTH`, `HEIGHT`: screen size in pixels.
* `screen`: the game window surface.
* `set_caption`: sets the window title.

---

### 3. **Colors**

```python
BLACK = (0, 0, 0)       # Background
GRAY = (50, 50, 50)     # Grid lines
WHITE = (255, 255, 255) # Score text
COLORS = [...]          # List of colors, each corresponding to a shape
```

Each shape will use one of these predefined colors.

---

### 4. **Shape Definitions**

```python
SHAPES = [
    [  # I shape (2 rotations)
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, -1), (1, 0), (1, 1), (1, 2)],
    ],
    ...
]
```

Each shape is defined as a list of rotations. Each rotation is a list of `(row, col)` offsets.

These offsets are relative to the top-left corner of the shape's bounding box.

---

### 5. **Board and Clock**

```python
clock = pygame.time.Clock()
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
```

* `board`: 2D list (matrix) to track locked-in pieces.

  * `0`: empty cell
  * `1-7`: occupied by a shape with a color index
* `clock`: used to regulate the game’s FPS (speed).

---

### 6. **Draw Board and Current Shape**

```python
def draw_board():
    screen.fill(BLACK)  # Clear screen
    ...
    pygame.display.flip()  # Update screen
```

* Draws:

  * Locked-in blocks (`board`)
  * The current falling shape (`current_shape`)
  * Grid lines
  * The score (`score_text`)

---

### 7. **Spawn a New Shape**

```python
def get_new_shape():
    shape_index = random.randint(0, len(SHAPES) - 1)
    rotation = 0
    shape = SHAPES[shape_index][rotation]
    start_col = COLS // 2 - 2
    coords = [(r, c + start_col) for r, c in shape]
    return coords, COLORS[shape_index], shape_index, rotation
```

* Randomly picks a shape and sets its initial position near the top center.
* Returns:

  * Coordinates of the blocks
  * Color
  * Index in SHAPES
  * Current rotation

---

### 8. **Valid Move Checker**

```python
def is_valid(shape):
    for r, c in shape:
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] != 0:
            return False
    return True
```

* Ensures the shape is inside the grid and not colliding with locked pieces.

---

### 9. **Movement Function**

```python
def move_shape(shape, dr, dc):
    moved = [(r + dr, c + dc) for r, c in shape]
    if is_valid(moved):
        return moved
    return shape
```

* Tries to move shape by `dr` rows and `dc` columns.
* Only moves if it’s valid.

---

### 10. **Rotation Function**

```python
def rotate_shape(shape_index, rotation, shape_pos):
    new_rotation = (rotation + 1) % len(SHAPES[shape_index])
    new_shape = SHAPES[shape_index][new_rotation]
    ...
    return rotated, new_rotation
```

* Rotates the shape by switching to the next rotation in `SHAPES`.
* Uses the first block in the shape as an anchor to preserve its relative position.
* If the rotated shape is valid, it's returned.

---

### 11. **Lock Shape Into Board**

```python
def lock_shape():
    for r, c in current_shape:
        board[r][c] = current_index + 1  # Save color index (1 to 7)
```

* Locks a shape into the board when it can no longer fall.

---

### 12. **Clear Full Lines + Score**

```python
def clear_lines():
    global board, score
    ...
    score += lines_cleared * 100
```

* Removes rows that are fully filled.
* Shifts everything above downward.
* Updates the score by 100 points per line.

---

### 13. **Initialize Game Variables**

```python
current_shape, current_color, current_index, current_rotation = get_new_shape()
fall_time = 0
fall_speed = 0.5
score = 0
font = pygame.font.SysFont('Arial', 24)
running = True
```

* These variables track:

  * The current falling shape
  * How fast it falls
  * The current score
  * The Pygame loop condition

---

### 14. **Main Game Loop**

```python
while running:
    fall_time += clock.get_rawtime()
    clock.tick()
    ...
```

* The game loop runs continuously while `running = True`.

#### ⏰ Auto-Fall:

```python
if fall_time / 1000 > fall_speed:
    moved = move_shape(current_shape, 1, 0)
    ...
```

* Every `fall_speed` seconds, the shape moves one row down.
* If it can’t, it locks in and a new shape spawns.

---

### 15. **Event Handling**

```python
for event in pygame.event.get():
    ...
    if event.key == pygame.K_LEFT: ...
    if event.key == pygame.K_UP:   ...
```

* Responds to:

  * ⬅️ Left: move left
  * ➡️ Right: move right
  * ⬇️ Down: speed up fall
  * ⬆️ Up: rotate shape

---

### 16. **Game Over Detection**

```python
if not is_valid(current_shape):
    print("Game Over!")
    running = False
```

* If a new shape can't be placed, the game ends.

---

### 17. **Quit Game**

```python
pygame.quit()
```

---


| Concept           | Description                                       |
| ----------------- | ------------------------------------------------- |
| `pygame` setup    | Initialize screen, handle input, draw shapes      |
| Grid logic        | Board represented with a 2D list                  |
| Shapes            | Defined using coordinates with multiple rotations |
| Game loop         | Controls game timing, input, and display          |
| Collision & logic | Valid movement, rotation, and locking             |
| Scoring           | Based on number of cleared lines                  |
| Game Over         | When a new piece doesn't fit                      |


