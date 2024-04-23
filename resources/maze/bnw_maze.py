import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30
WALL_COLOR = (0, 0, 0)        # Black
PATH_COLOR = (255, 255, 255)  # White
PLAYER_COLOR = (255, 0, 0)    # Red
GOAL_COLOR = (128, 128, 128)  # Gray

# Generate maze using Recursive Backtracking algorithm
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Set the outer border walls
    for y in range(height):
        for x in range(width):
            if x < 2 or x >= width - 2 or y < 2 or y >= height - 2:
                maze[y][x] = 1

    stack = [(2, 2)]  # Start the maze generation from an inner cell
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        neighbors = [(x + dx, y + dy) for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)] if 0 < x + dx < width - 2 and 0 < y + dy < height - 2 and (x + dx, y + dy) not in visited]

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
            visited.add((nx, ny))
        else:
            stack.pop()

    # Place the goal on the opposite side of the maze
    goal_y = random.choice([2, height - 3])  # Place the goal either at the top or bottom row
    goal_x = random.randint(2, width - 3)    # Randomly select a column for the goal
    maze[goal_y][goal_x] = 2  # Represent the goal with a different value

    return maze

# Generate a valid starting position for the player
def generate_start_position(maze):
    while True:
        player_x = random.randint(2, len(maze[0]) - 3)
        player_y = random.randint(2, len(maze) - 3)
        if maze[player_y][player_x] == 0:
            return player_x, player_y

# Function to reset the game
def reset_game():
    global maze, player_x, player_y, goal_x, goal_y
    maze = generate_maze(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
    player_x, player_y = generate_start_position(maze)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 2:
                goal_x, goal_y = x, y

# Generate maze
maze = generate_maze(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)

# Find goal position
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 2:
            goal_x, goal_y = x, y

# Find player position
player_x, player_y = generate_start_position(maze)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Decoy Maze Game")

# Main game loop
running = True
while running:
    screen.fill(WALL_COLOR)  # Fill screen with black

    # Draw maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = WALL_COLOR if maze[y][x] == 1 else PATH_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(screen, PLAYER_COLOR, (player_x * CELL_SIZE + CELL_SIZE // 2, player_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw goal
    pygame.draw.circle(screen, GOAL_COLOR, (goal_x * CELL_SIZE + CELL_SIZE // 2, goal_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Check for win condition
    if player_x == goal_x and player_y == goal_y:
        print("You win!")
        reset_game()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] != 1:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < len(maze) - 1 and maze[player_y + 1][player_x] != 1:
                player_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] != 1:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < len(maze[0]) - 1 and maze[player_y][player_x + 1] != 1:
                player_x += 1

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
