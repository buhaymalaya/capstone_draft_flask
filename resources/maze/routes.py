from . import bp

# embed py game into react using iframe with endpoint
from . import bnw_maze  

@bp.route('/maze-game')
def maze_game():
    # Use functionality from bnw_maze.py to generate and return the maze game content
    maze_content = bnw_maze.generate_maze()
    return maze_content