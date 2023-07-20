from pathlib import Path

from src.maze_solver.graphs.solver import (solve, solve_all)
# from src.maze_solver.models.border import Border
from src.maze_solver.models.maze import Maze
# from src.maze_solver.models.role import Role
# from src.maze_solver.models.square import Square
from src.maze_solver.models.solution import Solution
# from src.maze_solver.models.square import Square
from src.maze_solver.view.renderer import SVGRenderer


if __name__ == '__main__':
    # maze = Maze(
    #     squares=(
    #         Square(0, 0, 0, Border.TOP | Border.LEFT),
    #         Square(1, 0, 1, Border.TOP | Border.RIGHT),
    #         Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
    #         Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
    #         Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
    #         Square(5, 1, 1, Border.LEFT | Border.RIGHT),
    #         Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
    #         Square(7, 1, 3, Border.RIGHT),
    #         Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
    #         Square(9, 2, 1, Border.BOTTOM),
    #         Square(10, 2, 2, Border.TOP | Border.BOTTOM),
    #         Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),))

    # pathName = "./resource/miniature.maze"
    # pathName = "./resource/labyrinth.maze"
    pathName = "./resource/pacman_empty.maze"
    path = Path(pathName)
    maze = Maze.load(path)
    solution = solve_all(maze)

    print(solution)
    print("Length " + str(len(solution)))
    SVGRenderer().render(maze, solution[0]).preview()
    SVGRenderer().render(maze, solution[1]).preview()
    # print([square.index for square in solution])
    # print("width " + str(maze.width))
    # print("height " + str(maze.height))
    # print("length " + str(len(maze.squares)))
    # print("entrance " + str(maze.entrance))
    # print("exit " + str(maze.exit))

    # SVGRenderer().render(maze).preview()
    # dump(maze, Path(pathName))
    # solution = Solution(squares=tuple(maze[i] for i in (8, 11, 7, 6, 2)))
    # # svg = SVGRenderer().render(maze, solution)
    #
    # # with Path("maze.svg").open(mode="w", encoding="utf-8") as file:
    # #     file.write(svg.xml_content)
    #
    # renderer = SVGRenderer()
    # renderer.render(maze).preview()
    # renderer.render(maze, solution).preview()
