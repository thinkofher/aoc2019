#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import Dict
from copy import deepcopy
from math import ceil


Equation = Dict[str, int]
Equations = Dict[str, Equation]
MinimumValues = Dict[str, int]

FUEL = "FUEL"
ORE = "ORE"


def parse_equation(
    single_line: str, equations: Equations, mins: MinimumValues
) -> None:
    left_values, right_values = single_line.split(" => ")
    left = list(
        map(lambda val: tuple(val.split(" ")), left_values.split(", "))
    )

    right = tuple(right_values.split(" "))
    min_value, tag = right
    equations[tag] = {}
    mins[tag] = int(min_value)
    for value, subtag in left:
        equations[tag][subtag] = int(value)


def contains_only_ore(equation: Equation) -> bool:
    return len(equation) == 1 and list(equation.keys()) == ["ORE"]


def is_elemental(equation: Equation, equations: Equations) -> bool:
    return all(
        map(
            contains_only_ore,
            (equations[subtag] for subtag in equation.keys()),
        )
    )


def needed_multiplier(needed: int, min_value: int) -> int:
    return int(ceil(needed/min_value))


def add_equations(a: Equation, b: Equation) -> Equation:
    ans = deepcopy(a)
    for key, value in b.items():
        try:
            ans[key] += value
        except KeyError:
            ans[key] = value
    return ans


def multiply_equation(multiplier: int, equation: Equation) -> Equation:
    return {key: value * multiplier for key, value in equation.items()}


def execute_with_depth(
    eq: Equation, eqs: Equations, mins: MinimumValues, depth: int
) -> Equation:
    ans: Equation = {}
    for subtag, value in eq.items():
        if check_depth(eqs, subtag) == depth:
            ans = add_equations(
                ans,
                multiply_equation(
                    needed_multiplier(value, mins[subtag]),
                    eqs[subtag],
                )
            )
        else:
            ans = add_equations(ans, {subtag: value})
    return ans


def execute_deeply(eqs: Equations, mins: MinimumValues, tag: str) -> Equation:
    ans = deepcopy(eqs[tag])
    max_depth = check_depth(eqs, tag)
    while max_depth > 1:
        ans = execute_with_depth(ans, eqs, mins, max_depth)
        max_depth = max(
            map(
                lambda subtag: check_depth(eqs, subtag),
                ans.keys(),
            )
        )
    return ans


def check_depth(eqs: Equations, tag: str) -> int:
    if contains_only_ore(eqs[tag]):
        return 1
    else:
        ans = []
        for subtag in eqs[tag].keys():
            ans.append(check_depth(eqs, subtag))
        return max(ans) + 1


def solve_basic_equation(
    basic_equation: Equation, equations: Equations, mins: MinimumValues
) -> int:
    ans = 0
    for key, value in basic_equation.items():
        ans += equations[key][ORE] * needed_multiplier(value, mins[key])
    return ans


def calc_fuel(
    multiplier: int, equations: Equations, mins: MinimumValues
) -> int:
    equations["FUEL"] = multiply_equation(multiplier, equations["FUEL"])
    result = execute_deeply(equations, mins, "FUEL")
    fuel = solve_basic_equation(result, equations, mins)
    return fuel


def binary_search_fuel(eqs: Equations, mins: MinimumValues):
    target = 1000000000000
    lo = 1
    hi = 1000000000
    while lo <= hi:
        m = (lo + hi) // 2
        eqs_copy = deepcopy(eqs)
        val = calc_fuel(m, eqs_copy, mins)
        if val > target:
            hi = m - 1
        elif val < target:
            lo = m + 1
        else:
            return m
    return hi


def _main(args):
    equations: Equations = {}
    mins: MinimumValues = {}
    with open(args.filename, "r") as f:
        for line in map(lambda line: line.strip("\n"), f.readlines()):
            parse_equation(line, equations, mins)
    print(calc_fuel(1, equations, mins))
    print(binary_search_fuel(equations, mins))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 11th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    args = parser.parse_args()

    _main(args)
