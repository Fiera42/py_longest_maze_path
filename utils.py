def load_maze(filename):
    """
    Load the maze from a text file.
    """
    maze = []
    with open(filename, "r") as file:
        for line in file:
            maze.append([char for char in line.strip()])
    return maze


def is_valid_move(maze, row, col, visited):
    """
    Check if the move is valid.
    """
    rows = len(maze)
    cols = len(maze[0])
    return (
        0 <= row < rows
        and 0 <= col < cols
        and maze[row][col] != "1"
        and (row, col) not in visited
    )


def is_valid_path(maze, start, exit, path):
    """
    Check if the given path is valid according to certain rules.
    """
    # Rule 1: Path does not start at the starting square
    if path[0] != start:
        return False

    # Rule 2: Path does not end at the exit square
    if path[-1] != exit:
        return False

    # Rule 3: Path overlaps with itself
    if len(set(path)) != len(path):
        return False

    # Rule 4: Path has "jumps" in its pathing
    for i in range(len(path) - 1):
        row_diff = abs(path[i][0] - path[i + 1][0])
        col_diff = abs(path[i][1] - path[i + 1][1])
        if row_diff > 1 or col_diff > 1:
            return False

    # Rule 5: Path overlaps with a wall
    for row, col in path:
        if maze[row][col] == "1":
            return False

    # All rules passed, path is valid
    return True


def check_exit_reachable(maze, start, exit, visited):
    """
    Check if at least one square adjacent to the exit is reachable from the start.
    """
    # Create a dictionary to store adjacent cells for each cell
    adj_cells = {}
    rows, cols = len(maze), len(maze[0])
    for row in range(rows):
        for col in range(cols):
            adj_cells[(row, col)] = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if (
                    0 <= new_row < rows
                    and 0 <= new_col < cols
                    and maze[new_row][new_col] != "1"
                    and (new_row, new_col) not in visited
                ):
                    adj_cells[(row, col)].append((new_row, new_col))

    # Initialize a set to keep track of visited cells during traversal
    visited_during_traversal = set()

    # Start from the exit and traverse adjacent cells
    queue = [exit]
    while queue:
        cell = queue.pop(0)
        visited_during_traversal.add(cell)
        if cell == start:
            return True
        for neighbor in adj_cells[cell]:
            if neighbor not in visited_during_traversal and neighbor not in queue:
                queue.append(neighbor)

    return False


def duplicate_maze(maze):
    """
    Create a duplicate of the maze.
    """
    return [row[:] for row in maze]


def find_start_exit(maze):
    """
    Find the start and exit positions in the maze.
    """
    start = None
    exit = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j)
            elif maze[i][j] == "E":
                exit = (i, j)
    return start, exit


def visualize_path(maze, path):
    """
    Visualize the found path in a duplicate of the maze.
    """
    if not path:
        print("No path to visualize.")
        return

    # Duplicate the maze
    visualized_path = duplicate_maze(maze)

    # Replace empty spaces with "."
    visualized_path = [
        [cell.replace("0", ".") for cell in row] for row in visualized_path
    ]

    # Replace walls with "■"
    visualized_path = [
        [cell.replace("1", "■") for cell in row] for row in visualized_path
    ]

    # Define arrows for each direction
    arrows = {(-1, 0): "↑", (1, 0): "↓", (0, -1): "←", (0, 1): "→"}

    fallback_arrow = "?"  # Fallback arrow for unknown directions

    # Mark squares used by the path with arrows
    for i in range(1, len(path) - 1):
        (row, col), (next_row, next_col) = path[i], path[i + 1]
        direction = (next_row - row, next_col - col)
        visualized_path[row][col] = arrows.get(direction, fallback_arrow)

    # Print the visualized path
    print("\n")
    empty_spaces = 0
    for row in visualized_path:
        empty_spaces += row.count(".")
        print("".join(row))
    print(empty_spaces)
