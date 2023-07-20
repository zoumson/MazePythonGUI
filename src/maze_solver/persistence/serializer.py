import array
import pathlib
from typing import Iterator
#
# from src.maze_solver.models.border import Border
# from src.maze_solver.models.role import Role
# from src.maze_solver.models.square import Square
# from src.maze_solver.persistence.file_format import FileBody, FileHeader
from maze_solver.models.border import Border
from maze_solver.models.role import Role
from maze_solver.models.square import Square
from maze_solver.persistence.file_format import FileBody, FileHeader

FORMAT_VERSION: int = 1


def serialize(
    width: int,
    height: int,
    squares: tuple[Square, ...]
) -> tuple[FileHeader, FileBody]:

    # We had 2 components, first is header followed by the body
    # Header contains the magic number(MAZE), the format version
    # the maze width, the maze height
    # the body has each element/unit/square inside the maze compressed
    # completed using the map
    # return the header and the body
    header = FileHeader(FORMAT_VERSION, width, height)
    body = FileBody(array.array("B", map(compress, squares)))
    return header, body


def deserialize(header: FileHeader, body: FileBody) -> Iterator[Square]:
    # list is mutable, as we need a temporary storage to  keep appending
    # a newly created square, the unit maze data element
    # once the whole set of square retrieved from the file
    # it should be kept intact, this is achieved by converting the list into
    # tuple
    # the maze class takes a tuple as argument to build an instance of the class

    for index, square_value in enumerate(body.square_values):
        row, column = divmod(index, header.width)
        border, role = decompress(square_value)
        yield Square(index, row, column, border, role)


def compress(square: Square) -> int:
    # Encode the role first, then the border follows
    # border value is 4-bits data field
    # border role is a 3-bit data field
    # initially the role is store in the buffer
    #  which is  shifted left by 4 bits leaving
    #  a room for inserting the border using
    # the union operator
    # role = 5(decimal)
    # border = 11(decimal)
    # role = 101(binary)
    # border = 1011(binary)
    # role << 4 = 1010000
    # (role << 4)|border = (1010000) | (1011)
    #        1010000
    #     |  0001011
    #        1011011 ---> 7 bits
    # Data unit of information is 8-bits = byte
    # Need to add a leading 0
    # 1011011 ---> 7 bits ----> 01011011 ----> 8 bits
    # Return value is decimal format not binary
    return (square.role << 4) | square.border.value


def decompress(square_value: int) -> tuple[Border, Role]:
    # The last 4 bits/storage contain the border information
    # Use a masking to retrieve it applying the fetching operation via &
    # mask = 1111
    # Then shift right by 4 to erase the border room, now we can access
    # The role data
    # Get border first, then the role
    # border_role = 01011011
    # mask = 1111, in binary = 0b1111, in hex = 0xf
    # border = (border_role) & mask = (01011011) &  0xf = 1011
    # role = (border_role) >> 4 = 0101
    return Border(square_value & 0xf), Role(square_value >> 4)


def dump_squares(
    width: int,
    height: int,
    squares: tuple[Square, ...],
    path: pathlib.Path,
) -> None:

    # We take a maze data, build its header and body
    # The header has the magic number of the file format
    # followed by the file version, maze width, maze height
    # As for the body, each square in the maze is serialized from
    # its attached role and border
    # Obtained header and body are written into a binary file
    header, body = serialize(width, height, squares)
    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)


def load_squares(path: pathlib.Path) -> Iterator[Square]:
    # Read header first from the file
    # Inside the header make sure the magic number is included
    # Then check whether the file format version matched
    # Get the body data which have the sequence or alignment
    # of the square inside the maze
    # an enumeration provide the index
    # which combined with the width from the header helps to compute
    # the square row and column
    # the square value itself is decoded into role and border
    # finally a maze object is returned
    with path.open("rb") as file:
        header = FileHeader.read(file)
        if header.format_version != FORMAT_VERSION:
            raise ValueError("Unsupported file format version")
        body = FileBody.read(header, file)
        return deserialize(header, body)
