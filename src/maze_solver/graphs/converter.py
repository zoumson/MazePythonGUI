import math
from typing import NamedTuple, TypeAlias

import networkx as nx
#
# from src.maze_solver.models.border import Border
# from src.maze_solver.models.maze import Maze
# from src.maze_solver.models.role import Role
# from src.maze_solver.models.square import Square


from maze_solver.models.border import Border
from maze_solver.models.maze import Maze
from maze_solver.models.role import Role
from maze_solver.models.square import Square

Node: TypeAlias = Square


class Edge(NamedTuple):
    node1: Node
    node2: Node

    @property
    def flip(self) -> "Edge":
        return Edge(self.node2, self.node1)

    @property
    def distance(self) -> float:
        return math.dist(
            (self.node1.row, self.node1.column),
            (self.node2.row, self.node2.column)
        )

    # Bonus and float ranged from 1 to 100
    def weight(self, bonus: float = 20, penalty: float = 40) -> float:
        # We move from node 1 to node 1 in a directed graph
        # The outgoing node limits the movement if it has an enemy
        # it enforces the movement toward it if the latter has a reward
        match self.node2.role:
            case Role.REWARD:
                # return self.distance - bonus
                # return (1 - bonus / 100) * self.distance
                return  .0000000000000000000000001*self.distance
            case Role.ENEMY:
                # return (1 + penalty / 100) * self.distance
                return 100*self.distance
            case _:
                return self.distance*100


def get_nodes(maze: Maze) -> set[Node]:
    nodes: set[Node] = set()
    for square in maze:
        if square.role in (Role.EXTERIOR, Role.WALL):
            continue
        if square.role is not Role.NONE:
            nodes.add(square)
        if (
                square.border.intersection
                or square.border.dead_end
                or square.border.corner
        ):
            nodes.add(square)
    return nodes


def get_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    edges: set[Edge] = set()
    for source_node in nodes:
        # Follow right:
        node = source_node
        for x in range(node.column + 1, maze.width):
            if node.border & Border.RIGHT:
                break
            node = maze.squares[node.row * maze.width + x]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
        # Follow down:
        node = source_node
        for y in range(node.row + 1, maze.height):
            if node.border & Border.BOTTOM:
                break
            node = maze.squares[y * maze.width + node.column]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
    return edges


def make_graph(maze: Maze) -> nx.DiGraph:
    return nx.DiGraph(
        (edge.node1, edge.node2, {"weight": edge.weight()})
        for edge in get_directed_edges(maze, get_nodes(maze))
    )


def get_directed_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    # Get the undirected edges of the graph
    # For each edge, find its  corresponding flipped nodes
    # Undirected edge A -- B can be converted to 2 directed edges
    # A to B as A --> B and B to A as B --> A
    # edges = get_edges(maze, nodes) ---> initialization and assignment
    # for every edge in edges, flip it, then return the merged paired set
    # as original | flipped
    # The pipe operator | compute the union or concatenation of a set/dictionary

    return (edges := get_edges(maze, nodes)) | {edge.flip for edge in edges}
