#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List, NamedTuple, Set, Dict

ASTEROID = "#"
EMPTY = "."


class Point(NamedTuple):
    x: int
    y: int


class Vector(NamedTuple):
    x: float
    y: float

    def to_unit(self) -> 'Vector':
        return self.__class__(
            round(self.x / self.length(), 3),
            round(self.y / self.length(), 3))

    def length(self) -> float:
        return round((self.x**2 + self.y**2)**0.5, 3)

    @classmethod
    def from_two_points(cls, p1: Point, p2: Point) -> 'Vector':
        return cls(float(p2.x - p1.x), float(p2.y - p1.y))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 9th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    args = parser.parse_args()

    asteroid_map = []  # type: List[List[str]]
    with open(args.filename, "r") as f:
        for line in f.readlines():
            asteroid_map += [list(line.strip("\n"))]

    asteroids: Set[Point] = set()
    for y, verse in enumerate(asteroid_map):
        for x, value in enumerate(verse):
            if value == ASTEROID:
                asteroids.add(Point(x, y))

    vectors: Dict[Point, Set[Vector]] = {}

    for base in asteroids:
        for asteroid in (asteroids - set([base])):
            try:
                vectors[base].add(
                    Vector.from_two_points(base, asteroid).to_unit())
            except KeyError:
                vectors[base] = set(
                    [Vector.from_two_points(base, asteroid).to_unit()])

    detected_asteroids = {
        point: len(vec_set) for point, vec_set in vectors.items()
    }
    print(max(detected_asteroids.values()))
