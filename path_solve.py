import os
import random
from collections import deque
from tqdm import tqdm

from utils import (
    check_exit_reachable,
    duplicate_maze,
    find_start_exit,
    is_valid_move,
    is_valid_path,
    load_maze,
    visualize_path,
)


def find_path_wave_collapse(maze, start, exit):
    """
    Find the shortest path from start to exit in the maze using a modified wave function collapse algorithm.
    """
    if start is None or exit is None:
        return None  # If start or exit is not found, return None

    queue = deque(
        [(start, [])]
    )  # Initialize queue with start position and an empty path

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == exit:
            return path + [(row, col)]  # If exit is found, return the path

        visited = set(path)

        # Possible moves: up, down, left, right
        moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        # Check if any move directly leads to the exit and append it if found
        for new_row, new_col in moves:
            if (new_row, new_col) == exit:
                queue.appendleft(((new_row, new_col), path + [(row, col)]))
                break

        if not check_exit_reachable(maze, (row, col), exit, visited):
            continue

        random.shuffle(moves)

        visited = set(
            path + [(row, col)]
        )  # Add the current position to the visited set

        # Calculate the number of possible moves for each potential move
        move_counts = []
        for new_row, new_col in moves:
            new_moves = [
                (new_row - 1, new_col),
                (new_row + 1, new_col),
                (new_row, new_col - 1),
                (new_row, new_col + 1),
            ]
            if is_valid_move(maze, new_row, new_col, visited):
                valid_moves = sum(
                    is_valid_move(maze, r, c, visited) for r, c in new_moves
                )
                move_counts.append((new_row, new_col, valid_moves))

        # Sort the potential moves based on the number of possible moves
        move_counts.sort(key=lambda x: x[2], reverse=True)

        # Add the potential moves to the queue in sorted order
        for new_row, new_col, _ in move_counts:
            queue.appendleft(((new_row, new_col), path + [(row, col)]))

    return None  # If no path is found, return None


def create_longer_path(maze, shortest_path, depth=1):
    """
    Extend the initial shortest path to create a longer path.
    """
    # Randomly select start and end points on the initial path
    try:
        start_index = random.randint(
            1, len(shortest_path) - 2
        )  # Exclude the first and last points
    except:
        return shortest_path

    try:
        end_index = random.randint(1, len(shortest_path) - 2)
        if end_index < start_index:
            temp = end_index
            end_index = start_index
            start_index = temp
        elif end_index == start_index:
            end_index += 1
    except:
        return shortest_path

    start_point = shortest_path[start_index]
    end_point = shortest_path[end_index]

    # Rig the maze by blocking the squares in the sections that should act as walls
    rigged_maze = duplicate_maze(maze)
    wall_sections = shortest_path[:start_index] + shortest_path[end_index + 1 :]
    for row, col in wall_sections:
        rigged_maze[row][col] = "1"  # Mark the square as a wall

    next_row, next_col = shortest_path[start_index + 1]
    rigged_maze[next_row][next_col] = "1"  # Block the square after the start point

    # Find a new path between the start and end points
    new_path = find_path_wave_collapse(rigged_maze, start_point, end_point)

    if new_path is None:
        return shortest_path

    if depth > 0:
        for i in range(10):
            new_path = create_longer_path(rigged_maze, new_path, depth=depth - 1)

    # Combine the initial path and the new path
    longer_path = (
        shortest_path[:start_index] + new_path + shortest_path[end_index + 1 :]
    )

    if not is_valid_path(maze, shortest_path[0], shortest_path[-1], longer_path):
        return shortest_path
    elif len(shortest_path) >= len(longer_path):
        return shortest_path
    else:
        return longer_path


maze = load_maze(os.path.join("mazes", "maze_zig_zag.txt"))
start, exit = find_start_exit(maze)
if start is not None and exit is not None:
    shortest_path = find_path_wave_collapse(maze, start, exit)

    if shortest_path:
        for i in tqdm(range(10000)):
            prev = len(shortest_path)
            shortest_path = create_longer_path(maze, shortest_path, depth=5)
            if len(shortest_path) > prev:
                visualize_path(maze, shortest_path)
            # print(len(shortest_path))

        visualize_path(maze, shortest_path)

    else:
        print("No path found from start to exit.")


else:
    print("Start or exit not found in the maze.")
