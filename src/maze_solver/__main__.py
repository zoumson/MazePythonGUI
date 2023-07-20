import argparse
import pathlib

# from maze_solver.graphs.solver import solve_all
from maze_solver.graphs.solver import (solve_all, solve)
from maze_solver.models.maze import Maze
from maze_solver.view.renderer import SVGRenderer
#
# from src.maze_solver.graphs.solver import solve_all
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.view.renderer import SVGRenderer


def main() -> None:
    maze = Maze.load(parse_path())
    # solutions = solve_all(maze)
    solution = solve(maze)
    renderer = SVGRenderer()
    renderer.render(maze, solution).preview()
    # if solutions:
    #     renderer = SVGRenderer()
    #     for solution in solutions:
    #         renderer.render(maze, solution).preview()
    # else:
    #     print("No solution found")


def parse_path() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path)
    return parser.parse_args().path


if __name__ == "__main__":
    main()
