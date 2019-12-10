#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
import networkx as nx

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 6th day of Advent of Code.",
    )
    parser.add_argument(
        "filename",
        metavar="f",
        type=str,
        help="name of the file with input data",
    )
    args = parser.parse_args()

    graph = nx.DiGraph()

    with open(args.filename, "r") as f:
        for line in map(lambda line: line.strip("\n"), f.readlines()):
            planets = line.split(")")
            graph.add_edge(planets[1], planets[0])

    bfs_calculated_nodes = [
        list(nx.bfs_tree(graph, node))[1:] for node in graph.nodes()
    ]
    print(sum(map(len, bfs_calculated_nodes)))
    path = list(
        nx.algorithms.simple_paths.shortest_simple_paths(
            graph.to_undirected(), "YOU", "SAN"
        )
    )[0]
    print(len(list(zip(path[1:-1], path[2:-1]))))
