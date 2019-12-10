#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
from typing import List
import argparse
import enum


@enum.unique
class Color(enum.Enum):
    Black = 0
    White = 1
    Transparent = 2

    @staticmethod
    def visualize(color) -> str:
        if color == Color.Transparent:
            return '?'
        if color == Color.Black:
            return '.'
        if color == Color.White:
            return 'x'


def check_for_corruption(chunked_image_data: List[List[Color]]) -> int:
    data = chunked_image_data[:]
    data.sort(key=lambda lst: lst.count(Color.Black))
    return data[0].count(Color.Transparent) * data[0].count(Color.White)


def remove_transparent(image_data: List[Color]) -> List[Color]:
    return list(filter(lambda pixel: pixel != Color.Transparent, image_data))


def visualize(image: List[Color], width: int) -> str:
    pixels = list(map(Color.visualize, image))
    pixels_chunks = chunks(pixels, width)
    return '\n'.join(map(lambda lst: ''.join(lst), pixels_chunks))


def get_top_visible_pixels(
    chunked_image_data: List[List[Color]],
) -> List[Color]:

    pixels_columns = [
        [lst.pop(0) for lst in image_data_chunked[:]]
        for _ in range(len(image_data_chunked[0]))
    ]
    pixels_without_transparent = map(remove_transparent, pixels_columns)
    top_pixels = [lst.pop(0) for lst in pixels_without_transparent]
    return top_pixels


def chunks(lst, n: int):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 7th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    parser.add_argument(
        "--width", type=int, help="image width", default=25,
    )
    parser.add_argument(
        "--height", type=int, help="image height", default=6,
    )
    args = parser.parse_args()

    image_data = []
    with open(args.filename, "r") as f:
        for line in f.readlines():
            image_data += list(
                map(lambda value: Color(int(value)), line.strip("\n"))
            )

    image_data_chunked = chunks(image_data, args.height * args.width)
    print(check_for_corruption(image_data_chunked))

    visible_pixels = get_top_visible_pixels(image_data_chunked)
    print(visualize(visible_pixels, args.width))
