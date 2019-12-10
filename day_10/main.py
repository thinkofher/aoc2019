#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List, NamedTuple, Set, Dict, Tuple
from math import acos, pi

ASTEROID = "#"
EMPTY = "."
PRECISION = 3


class Point(NamedTuple):
    x: int
    y: int


class Vector(NamedTuple):
    x: float
    y: float

    def to_unit(self) -> 'Vector':
        return self.__class__(
            round(self.x / self.length(), PRECISION),
            round(self.y / self.length(), PRECISION))

    def length(self) -> float:
        return round((self.x**2 + self.y**2)**0.5, PRECISION)

    @property
    def angle_from_origin(self) -> float:
        origin_x = -1
        origin_y = 0

        return round(
            acos((origin_x * self.x + origin_y * self.y)/(self.length()))
            * (180/pi), PRECISION)

    @classmethod
    def from_two_points(cls, p1: Point, p2: Point) -> 'Vector':
        return cls(float(p2.x - p1.x), float(p2.y - p1.y))


def parse_asteroids(asteroid_map: List[List[str]]) -> Set[Point]:
    asteroids = set()
    for y, verse in enumerate(asteroid_map):
        for x, value in enumerate(verse):
            if value == ASTEROID:
                asteroids.add(Point(x, y))
    return asteroids


def calculate_vectors(asteroids: Set[Point]) -> Dict[Point, Set[Vector]]:
    vectors = {}
    for base in asteroids:
        for asteroid in (asteroids - set([base])):
            try:
                vectors[base].add(
                    Vector.from_two_points(base, asteroid).to_unit())
            except KeyError:
                vectors[base] = set(
                    [Vector.from_two_points(base, asteroid).to_unit()])
    return vectors


def find_best_base(vectors_map: Dict[Point, Set[Vector]]) -> Tuple[Point, int]:
    detected_asteroids: Dict[Point, int] = {
        point: len(vec_set) for point, vec_set in vectors_map.items()
    }
    best_result = max(detected_asteroids.values())
    points_by_detected_asteroids = {
        value: key for key, value in detected_asteroids.items()
    }

    return points_by_detected_asteroids[best_result], best_result


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

    asteroids = parse_asteroids(asteroid_map)
    vectors = calculate_vectors(asteroids)

    base, best_result = find_best_base(vectors)
    print(best_result)
