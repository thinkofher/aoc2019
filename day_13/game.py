import enum
from typing import List, Dict, NamedTuple

from handler import IOHandler


@enum.unique
class Tile(enum.Enum):
    Empty = 0
    Wall = 1
    Block = 2
    HorizontalPaddle = 3
    Ball = 4


class Position(NamedTuple):
    from_left: int
    from_top: int


Tiles = Dict[Position, Tile]


def find_tile_position(tiles: Tiles, ftile: Tile) -> Position:
    for position, tile in tiles.items():
        if tile == ftile:
            return position


def find_player_position(tiles: Tiles) -> Position:
    return find_tile_position(tiles, Tile.HorizontalPaddle)


def find_ball_position(tiles: Tiles) -> Position:
    return find_tile_position(tiles, Tile.Ball)


def visualize_table(tiles: Tiles) -> None:
    max_x = max(map(lambda p: p.from_left, tiles.keys()))
    min_x = min(map(lambda p: p.from_left, tiles.keys()))
    max_y = max(map(lambda p: p.from_top, tiles.keys()))
    min_y = min(map(lambda p: p.from_top, tiles.keys()))

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            tile = Tile.Empty
            try:
                tile = tiles[Position(x, y)]
            except KeyError:
                pass

            if tile == Tile.Wall:
                print('|', end='')
            elif tile == Tile.HorizontalPaddle:
                print('_', end='')
            elif tile == Tile.Ball:
                print('o', end='')
            elif tile == Tile.Block:
                print('x', end='')
            else:
                print('.', end='')
        print('\n', end='')
    for i in range(0, max_x):
        print(i % 9, end='')
    print('\n', end='')


def chunks(lst, n: int):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


class IOGame(IOHandler):

    output_values: List[int] = []
    relative_base_adjust_value: int = 0
    tiles: Tiles = {}

    def get_input(self) -> int:
        visualize_table(self.tiles)
        move = 100

        while move not in (-1, 0, 1):
            try:
                move = int(input("What's your move (-1, 0, 1): "))
            except ValueError:
                move = 0

        return move

    def set_output(self, value: int) -> None:
        self.output_values.append(value)

        if len(self.output_values) == 3:
            left, top, id = tuple(self.output_values)

            if left == -1 and top == 0:
                print('Your score: ', id)
            else:
                self.tiles[Position(left, top)] = Tile(id)

            self.output_values = []
