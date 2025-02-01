import pygame
import random
import json
from PIL import Image
import glob
import os
import argparse 

class Maze:
    def __init__(self, grid_width, grid_height, cell_size):
        """Initializes the Maze."""
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.width = grid_width * cell_size
        self.height = grid_height * cell_size
        self.cells = self._create_grid()
        self.start_cell = self.cells[0][0]
        self.end_cell = self.cells[grid_height - 1][grid_width - 1]
        self.path = []

    def _create_grid(self):
        """Creates a grid of cells for the maze."""
        cells = [[Cell(row, col) for col in range(self.grid_width)] for row in range(self.grid_height)]
        return cells

    def generate_maze_recursive_backtracking(self):
        """Generates a maze using recursive backtracking."""
        start_cell = self.cells[0][0]
        stack = [start_cell]
        start_cell.visited = True

        while stack:
            current_cell = stack[-1]
            unvisited_neighbors = self._get_unvisited_neighbors(current_cell)

            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                self._break_walls(current_cell, neighbor)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()
        self._reset_visited()

    def _reset_visited(self):
        """Resets the visited status of all cells."""
        for row_cells in self.cells:
            for cell in row_cells:
                cell.visited = False

    def _get_unvisited_neighbors(self, cell):
        """Gets unvisited neighbors of a cell."""
        neighbors = []
        row, col = cell.row, cell.col

        if row > 0 and not self.cells[row - 1][col].visited:
            neighbors.append(self.cells[row - 1][col])
        if col < self.grid_width - 1 and not self.cells[row][col + 1].visited:
            neighbors.append(self.cells[row][col + 1])
        if row < self.grid_height - 1 and not self.cells[row + 1][col].visited:
            neighbors.append(self.cells[row + 1][col])
        if col > 0 and not self.cells[row][col - 1].visited:
            neighbors.append(self.cells[row][col - 1])

        return neighbors

    def _break_walls(self, cell1, cell2):
        """Breaks walls between two adjacent cells."""
        row1, col1 = cell1.row, cell1.col
        row2, col2 = cell2.row, cell2.col

        if row1 < row2:
            cell1.walls["S"] = False
            cell2.walls["N"] = False
        elif row1 > row2:
            cell1.walls["N"] = False
            cell2.walls["S"] = False
        elif col1 < col2:
            cell1.walls["E"] = False
            cell2.walls["W"] = False
        elif col1 > col2:
            cell1.walls["W"] = False
            cell2.walls["E"] = False

    def solve_maze_dfs(self):
        """Solves the maze using Depth-First Search algorithm."""
        self._reset_visited()
        stack = [(self.start_cell, [self.start_cell])]

        while stack:
            current_cell, current_path = stack.pop()

            if current_cell == self.end_cell:
                self.path = current_path
                return True

            current_cell.visited = True

            row, col = current_cell.row, current_cell.col

            if row > 0 and not current_cell.walls["N"] and not self.cells[row - 1][col].visited:
                stack.append((self.cells[row - 1][col], current_path + [self.cells[row - 1][col]]))

            if col < self.grid_width - 1 and not current_cell.walls["E"] and not self.cells[row][col + 1].visited:
                stack.append((self.cells[row][col + 1], current_path + [self.cells[row][col + 1]]))

            if row < self.grid_height - 1 and not current_cell.walls["S"] and not self.cells[row + 1][col].visited:
                stack.append((self.cells[row + 1][col], current_path + [self.cells[row + 1][col]]))

            if col > 0 and not current_cell.walls["W"] and not self.cells[row][col - 1].visited:
                stack.append((self.cells[row][col - 1], current_path + [self.cells[row][col - 1]]))

        return False


    def draw_tile_to_surface(self, surface, wall_color, cell_color, start_color, end_color, border_color, path_color, tile_row_start, tile_row_end, tile_col_start, tile_col_end, draw_solution=False):
        """Draws a portion (tile) of the maze on a Pygame Surface, optionally with solution path."""
        for row in range(tile_row_start, tile_row_end):
            for col in range(tile_col_start, tile_col_end):
                cell = self.cells[row][col]
                is_start = (cell == self.start_cell)
                is_end = (cell == self.end_cell)
                is_path = draw_solution and (cell in self.path)
                cell.draw_to_surface(surface, self.cell_size, wall_color, cell_color, start_color, end_color, path_color, is_start, is_end, is_path, tile_offset_x=tile_col_start * self.cell_size, tile_offset_y=tile_row_start * self.cell_size)


    def to_json_serializable(self):
        """Converts the maze data to a JSON serializable format."""
        maze_data = {
            "grid_width": self.grid_width,
            "grid_height": self.grid_height,
            "cell_size": self.cell_size,
            "cells": []
        }
        for row_cells in self.cells:
            row_data = []
            for cell in row_cells:
                row_data.append({
                    "row": cell.row,
                    "col": cell.col,
                    "walls": cell.walls
                })
            maze_data["cells"].append(row_data)
        return maze_data

    @staticmethod
    def from_json_data(json_data):
        """Creates a Maze object from JSON data."""
        grid_width = json_data["grid_width"]
        grid_height = json_data["grid_height"]
        cell_size = json_data["cell_size"]
        maze = Maze(grid_width, grid_height, cell_size)
        cells_data = json_data["cells"]
        for row_index, row_data in enumerate(cells_data):
            for col_index, cell_data in enumerate(row_data):
                cell = maze.cells[row_index][col_index]
                cell.walls = cell_data["walls"]
        return maze


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {"N": True, "E": True, "S": True, "W": True}
        self.visited = False

    def draw_to_surface(self, surface, cell_size, wall_color, cell_color, start_color, end_color, path_color, is_start=False, is_end=False, is_path=False, tile_offset_x=0, tile_offset_y=0):
        """Draws the cell on a Pygame Surface, optionally marking start/end/path, with tile offset."""
        x = self.col * cell_size - tile_offset_x
        y = self.row * cell_size - tile_offset_y

        pygame.draw.rect(surface, cell_color, (x, y, cell_size, cell_size))

        if is_start:
            pygame.draw.rect(surface, start_color, (x, y, cell_size, cell_size))
        elif is_end:
            pygame.draw.rect(surface, end_color, (x, y, cell_size, cell_size))
        elif is_path:
            pygame.draw.rect(surface, path_color, (x, y, cell_size, cell_size))


        if self.walls["N"]:
            pygame.draw.line(surface, wall_color, (x, y), (x + cell_size, y), 2)
        if self.walls["E"]:
            pygame.draw.line(surface, wall_color, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if self.walls["S"]:
            pygame.draw.line(surface, wall_color, (x, y + cell_size), (x + cell_size, y + cell_size), 2)
        if self.walls["W"]:
            pygame.draw.line(surface, wall_color, (x, y), (x, y + cell_size), 2)

def generate_maze_image_and_json_tiled_combined(maze: Maze, grid_cols, grid_rows, cell_size, filename_base="maze", tile_width_cells=100, tile_height_cells=100, draw_solution=False, tile=True):
    """Generates a maze, saves JSON, tiled PNGs, and combines tiles into one large PNG (no window), optionally with solution path."""

    pygame.init()


    if draw_solution:
        maze.solve_maze_dfs()

    wall_color = (0, 0, 0)
    background_color = (255, 255, 255)
    cell_color = background_color
    start_color = (0, 255, 0)
    end_color = (255, 0, 0)
    border_color = (0, 0, 0)
    path_color = (0, 0, 255)

    if tile:
        num_tile_cols = (grid_cols + tile_width_cells - 1) // tile_width_cells
        num_tile_rows = (grid_rows + tile_height_cells - 1) // tile_height_cells

        tile_images = []

        for tile_row_index in range(num_tile_rows):
            tile_images_row = []
            for tile_col_index in range(num_tile_cols):
                tile_filename = f"{filename_base}_tile_{tile_row_index}_{tile_col_index}.png"
                print(f"Generating tile: {tile_filename}")

                tile_row_start = tile_row_index * tile_height_cells
                tile_row_end = min((tile_row_index + 1) * tile_height_cells, grid_rows)
                tile_col_start = tile_col_index * tile_width_cells
                tile_col_end = min((tile_col_index + 1) * tile_width_cells, grid_cols)

                tile_width_pixels = (tile_col_end - tile_col_start) * cell_size
                tile_height_pixels = (tile_row_end - tile_row_start) * cell_size

                tile_surface = pygame.Surface((tile_width_pixels, tile_height_pixels))
                tile_surface.fill(background_color)

                maze.draw_tile_to_surface(tile_surface, wall_color, cell_color, start_color, end_color, border_color, path_color, tile_row_start, tile_row_end, tile_col_start, tile_col_end, draw_solution)

                pygame.image.save(tile_surface, tile_filename)
                print(f"Tile image saved to '{tile_filename}'")

                tile_image_pil = Image.open(tile_filename)
                tile_images_row.append(tile_image_pil)

            tile_images.append(tile_images_row)
        combined_image_filename = f"{filename_base}_combined.png"

        combined_width_pixels = grid_cols * cell_size
        combined_height_pixels = grid_rows * cell_size
        combined_image_pil = Image.new('RGB', (combined_width_pixels, combined_height_pixels), color=background_color)

        for tile_row_index in range(num_tile_rows):
            for tile_col_index in range(num_tile_cols):
                tile_image_pil = tile_images[tile_row_index][tile_col_index]
                x_offset = tile_col_index * tile_width_cells * cell_size
                y_offset = tile_row_index * tile_height_cells * cell_size
                combined_image_pil.paste(tile_image_pil, (x_offset, y_offset))

        combined_image_pil.save(combined_image_filename)
        print(f"Combined maze image saved to '{combined_image_filename}'")

        for file in glob.glob(f'{filename_base}_tile_*_*.png'):
            os.remove(file)

    else: 
        image_filename = f"{filename_base}.png"
        surface = pygame.Surface((grid_cols * cell_size, grid_rows * cell_size))
        surface.fill(background_color)
        maze.draw_tile_to_surface(surface, wall_color, cell_color, start_color, end_color, border_color, path_color, 0, grid_rows, 0, grid_cols, draw_solution)
        pygame.image.save(surface, image_filename)
        print(f"Single maze image saved to '{image_filename}'")

    #maze_json_filename = f"{filename_base}.json"
    #with open(maze_json_filename, 'w') as f:
    #    json.dump(maze.to_json_serializable(), f, indent=4)
    #print(f"Maze JSON data saved to '{maze_json_filename}'")

    pygame.quit()



def main():
    parser = argparse.ArgumentParser(description="Generate a maze and save it as an image and JSON.")
    parser.add_argument("-W", "--width", type=int, default=20, help="Width of the maze (number of columns)")
    parser.add_argument("-H", "--height", type=int, default=20, help="Height of the maze (number of rows)")
    parser.add_argument("-c", "--cell-size", type=int, default=10, help="Size of each cell in pixels")
    parser.add_argument("-t", "--tile-size", type=int, default=200, help="Tile size in cells for tiling (used if tiling is enabled)")
    parser.add_argument("-n", "--filename-base", type=str, default="large_maze", help="Base filename for output files (image and JSON)")
    parser.add_argument("-s", "--solve", action="store_true", default=False, help="Solve the maze and draw the solution path")
    parser.add_argument("--no-tiling", action="store_true", default=False, help="Disable tiling and generate a single image")

    args = parser.parse_args()

    grid_cols = args.width
    grid_rows = args.height
    cell_size = args.cell_size
    tile_size_cells = args.tile_size
    filename_base = args.filename_base
    draw_solution = args.solve
    tile = not args.no_tiling 

    maze = Maze(grid_cols, grid_rows, cell_size)
    maze.generate_maze_recursive_backtracking()

    if tile:
        filename_base_normal = f"{filename_base}_normal"
        filename_base_solved = f"{filename_base}_solved"

        generate_maze_image_and_json_tiled_combined(maze, grid_cols, grid_rows, cell_size, filename_base_normal, tile_width_cells=tile_size_cells, tile_height_cells=tile_size_cells, draw_solution=False, tile=tile)

        if draw_solution:
            generate_maze_image_and_json_tiled_combined(maze, grid_cols, grid_rows, cell_size, filename_base_solved, tile_width_cells=tile_size_cells, tile_height_cells=tile_size_cells, draw_solution=True, tile=tile)

        for file in glob.glob(f'{filename_base_normal}_tile_*_*.png') + glob.glob(f'{filename_base_solved}_tile_*_*.png'):
            os.remove(file)
    else: 
        filename_base_output = filename_base
        if draw_solution:
            filename_base_output = f"{filename_base}_solved"
        generate_maze_image_and_json_tiled_combined(maze, grid_cols, grid_rows, cell_size, filename_base_output, draw_solution=draw_solution, tile=tile)


if __name__ == "__main__":
    main()