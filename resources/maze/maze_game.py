import pygame
import sys
import random
from flask import Flask, jsonify

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30
WALL_COLOR = (0, 0, 0)        # Black
PATH_COLOR = (255, 255, 255)  # White
PLAYER_COLOR = (255, 0, 0)    # Red
GOAL_COLOR = (128, 128, 128)  # Gray

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Decoy Maze Game")

class MazeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = self.generate_maze()
        self.find_goal_position()
        self.player_x, self.player_y = self.generate_start_position()

    # Generate maze using Recursive Backtracking algorithm
    def generate_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Set the outer border walls
        for y in range(self.height):
            for x in range(self.width):
                if x < 2 or x >= self.width - 2 or y < 2 or y >= self.height - 2:
                    maze[y][x] = 1

        stack = [(2, 2)]  # Start the maze generation from an inner cell
        visited = set(stack)

        while stack:
            x, y = stack[-1]
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)] if 0 < x + dx < self.width - 2 and 0 < y + dy < self.height - 2 and (x + dx, y + dy) not in visited]

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[ny][nx] = 0
                maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                stack.pop()

        # Place the goal on the opposite side of the maze
        goal_y = random.choice([2, self.height - 3])  # Place the goal either at the top or bottom row
        goal_x = random.randint(2, self.width - 3)    # Randomly select a column for the goal
        maze[goal_y][goal_x] = 2  # Represent the goal with a different value

        return maze

    # Generate a valid starting position for the player
    def generate_start_position(self):
        while True:
            player_x = random.randint(2, len(self.maze[0]) - 3)
            player_y = random.randint(2, len(self.maze) - 3)
            if self.maze[player_y][player_x] == 0:
                return player_x, player_y

    # Function to reset the game
    def reset_game(self):
        self.maze = self.generate_maze()
        self.player_x, self.player_y = self.generate_start_position()
        self.find_goal_position()

    # Find goal position
    def find_goal_position(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 2:
                    self.goal_x, self.goal_y = x, y

# Initialize the game
game = MazeGame(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)

app = Flask(__name__)

# Route to serve maze game state as JSON
@app.route('/maze/game_state')
def get_game_state():
    return jsonify({
        'maze': game.maze,
        'player_position': (game.player_x, game.player_y),
        'goal_position': (game.goal_x, game.goal_y)
    })



# Main game loop
running = True
while running:
    screen.fill(WALL_COLOR)  # Fill screen with black

    # Draw maze
    for y in range(len(game.maze)):
        for x in range(len(game.maze[y])):
            color = WALL_COLOR if game.maze[y][x] == 1 else PATH_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(screen, PLAYER_COLOR, (game.player_x * CELL_SIZE + CELL_SIZE // 2, game.player_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw goal
    pygame.draw.circle(screen, GOAL_COLOR, (game.goal_x * CELL_SIZE + CELL_SIZE // 2, game.goal_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Check for win condition
    if game.player_x == game.goal_x and game.player_y == game.goal_y:
        print("You win!")
        game.reset_game()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.player_y > 0 and game.maze[game.player_y - 1][game.player_x] != 1:
                game.player_y -= 1
            elif event.key == pygame.K_DOWN and game.player_y < len(game.maze) - 1 and game.maze[game.player_y + 1][game.player_x] != 1:
                game.player_y += 1
            elif event.key == pygame.K_LEFT and game.player_x > 0 and game.maze[game.player_y][game.player_x - 1] != 1:
                game.player_x -= 1
            elif event.key == pygame.K_RIGHT and game.player_x < len(game.maze[0]) - 1 and game.maze[game.player_y][game.player_x + 1] != 1:
                game.player_x += 1

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

