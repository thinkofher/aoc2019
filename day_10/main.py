#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from itertools import cycle
from typing import List, NamedTuple, Set, Dict, Tuple
from math import acos, pi

ASTEROID = "#"
EMPTY = "."
PRECISION = 3


class Point(NamedTuple):
    x: int
    y: int

    def distance(self, other: "Point") -> float:
        return round(
            ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5,
            PRECISION,
        )


class Vector(NamedTuple):
    x: float
    y: float

    def to_unit(self) -> "Vector":
        return self.__class__(
            round(self.x / self.length(), PRECISION),
            round(self.y / self.length(), PRECISION),
        )

    def length(self) -> float:
        return round((self.x ** 2 + self.y ** 2) ** 0.5, PRECISION)

    @property
    def angle_from_origin(self) -> float:
        origin_x = 0
        origin_y = -1

        angle = round(
            acos((origin_x * self.x + origin_y * self.y) / (self.length()))
            * (180 / pi),
            PRECISION,
        )
        if self.x >= 0:
            return angle
        else:
            return 360 - angle

    @classmethod
    def from_two_points(cls, p1: Point, p2: Point) -> "Vector":
        return cls(float(p2.x - p1.x), float(p2.y - p1.y))


def parse_asteroids(asteroid_map: List[List[str]]) -> Set[Point]:
    asteroids = set()
    for y, verse in enumerate(asteroid_map):
        for x, value in enumerate(verse):
            if value == ASTEROID:
                asteroids.add(Point(x, y))
    return asteroids


def calculate_vectors(asteroids: Set[Point]) -> Dict[Point, Set[Vector]]:
    vectors: Dict[Point, Set[Vector]] = {}
    for base in asteroids:
        for asteroid in asteroids - set([base]):
            new_vector = Vector.from_two_points(base, asteroid).to_unit()
            try:
                vectors[base].add(new_vector)
            except KeyError:
                vectors[base] = set([new_vector])
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


def seek_for_targets_around_baes(
    base: Point, asteroids: Set[Point]
) -> Dict[Vector, List[Point]]:

    points_by_vector: Dict[Vector, List[Point]] = {}

    for asteroid in asteroids - set([base]):
        vec = Vector.from_two_points(base, asteroid).to_unit()
        try:
            points_by_vector[vec].append(asteroid)
            points_by_vector[vec].sort(key=lambda point: base.distance(point))
        except KeyError:
            points_by_vector[vec] = [asteroid]

    sorted_vectors = sorted(
        points_by_vector.keys(), key=lambda vec: vec.angle_from_origin
    )
    points_by_vector = {vec: points_by_vector[vec] for vec in sorted_vectors}

    return points_by_vector


def vaporize_sorted_asteroids(
    points_by_vector: Dict[Vector, List[Point]]
) -> Tuple[Point, ...]:

    result = []
    for vec in cycle(points_by_vector.keys()):
        # if every list in dict is empty
        if not sum(map(len, points_by_vector.values())):
            break
        try:
            result.append(points_by_vector[vec].pop(0))
        except IndexError:
            continue
    return tuple(result)


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
    print(
        f"The best location for a new monitoring \
base is at {base.x},{base.y}.",
        end=" ",
    )
    print(f"{best_result} asteroids detected.")

    targets = seek_for_targets_around_baes(base, asteroids)
    ready_to_destroy = vaporize_sorted_asteroids(targets)
    n = 200
    n_asteroid = ready_to_destroy[n - 1]
    answer = 100 * n_asteroid.x + n_asteroid.y
    print(
        f"The {n}th asteroid to be vaporized is \
at {n_asteroid.x},{n_asteroid.y}.",
        end=" ",
    )
    print(f"Puzzle answer is {answer}.")
