# Python Maze Generator

This project is a maze generator written in Python using the Pygame library for graphics and PIL (Pillow) for image manipulation. It can generate mazes of various sizes and save them as PNG images, as well as JSON files to store the maze structure.

## Features

- **Maze Generation:** Uses a recursive backtracking algorithm to generate mazes.
- **Save as PNG:** Mazes can be saved as PNG images.
- **Tile Generation:** Supports tiled maze generation to generate very large mazes.
- **Maze Solver:** Can optionally solve the maze and display the solution path.
- **Save as JSON:** The maze structure can be saved to a JSON file.
- **Configuration via command line arguments:** Easily configurable parameters such as maze size, cell size, etc.

## Dependencies

- Python 3.6+
- Pygame
- Pillow (PIL)

You can install dependencies with the command:

```bash
pip install pygame pillow
```

## Usage

### Run

To run the script, use the following command:

```bash
python maze.py [options]
```

### Options

- `-W`, `--width`: The width of the maze (number of columns). Default: 20.
- `-H`, `--height`: The height of the maze (number of rows). Default: 20.
- `-c`, `--cell-size`: The size of each cell in pixels. Default: 10.
- `-t`, `--tile-size`: Tile size in cells (used if tiling is enabled). Default: 200.
- `-n`, `--filename-base`: Base filename for output files (image and JSON). Default: "large\_maze".
- `-s`, `--solve`: Solve the maze and display the solution path.
- `--no-tiling`: Disable tiling and generate a single image.

### Examples

1. **Create a 50x50 maze with a cell size of 15, save to file "my_maze.png", without solving:**

```bash
python maze.py -W 50 -H 50 -c 15 -n my_maze
```

2. **Create a 100x100 maze with a cell size of 10, split into 100x100 tiles, save to files "large_maze_combined.png" and "large_maze_solved_combined.png", with solving:**

```bash
python maze.py -W 100 -H 100 -c 10 -t 100 -n large_maze -s
```

3. **Create a 30x30 maze with a cell size of 20, without tiles, without solutions:**

```bash
python maze.py -W 30 -H 30 -c 20 -n small_maze --no-tiling
```

## Code Structure

- `maze.py`: The main script that contains the `Maze` and `Cell` classes, as well as functions for generating and saving mazes.

## How it works

1. **`Cell` class:** Represents a single cell in the maze, stores information about walls and visited status.
2. **`Maze` class:**
- Initializes the maze by creating a grid of cells.
- Generates the maze using a recursive backtracking algorithm.
- Solves the maze using a depth-first search (DFS) algorithm.
- Draws the maze on a Pygame Surface, with the ability to tile and display the solution.
- Saves the maze as JSON.
3. **Function `generate_maze_image_and_json_tiled_combined`:**
- Creates a Pygame Surface for drawing the maze.
- Draws the maze, cell by cell.
- Saves the image as PNG.
- Saves the maze structure as JSON.
4. **Function `main`:**
- Processes command line arguments.
- Creates a `Maze` object.
- Calls functions to generate, solve, and save the maze.

