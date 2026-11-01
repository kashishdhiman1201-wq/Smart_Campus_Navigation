
import time
import pandas as pd
import matplotlib.pyplot as plt

from modules.graph_builder import create_campus_graph
from algorithms.dijkstra import dijkstra
from algorithms.a_star import a_star
from algorithms.bfs_dfs import bfs, dfs


def compare_algorithms():

    graph = create_campus_graph()

    start = "MAIN_GATE"
    destination = "COMPUTER_LAB"

    results = []

    # Dijkstra
    dijkstra_result = dijkstra(graph, start, destination)

    results.append({
        "Algorithm": "Dijkstra",
        "Execution Time (ms)": dijkstra_result["execution_time"] * 1000,
        "Visited Nodes": dijkstra_result["visited_nodes"],
        "Distance (m)": dijkstra_result["distance"],
        "Status": dijkstra_result["status"]
    })

    # A*
    astar_result = a_star(graph, start, destination)

    results.append({
        "Algorithm": "A*",
        "Execution Time (ms)": astar_result["execution_time"] * 1000,
        "Visited Nodes": astar_result["visited_nodes"],
        "Distance (m)": astar_result["distance"],
        "Status": astar_result["status"]
    })

    # BFS
    bfs_result = bfs(graph, start)

    results.append({
        "Algorithm": "BFS",
        "Execution Time (ms)": bfs_result["execution_time"] * 1000,
        "Visited Nodes": len(bfs_result["traversal"]),
        "Distance (m)": None,
        "Status": bfs_result["status"]
    })

    # DFS
    dfs_result = dfs(graph, start)

    results.append({
        "Algorithm": "DFS",
        "Execution Time (ms)": dfs_result["execution_time"] * 1000,
        "Visited Nodes": len(dfs_result["traversal"]),
        "Distance (m)": None,
        "Status": dfs_result["status"]
    })

    df = pd.DataFrame(results)

    print("\n========== ALGORITHM PERFORMANCE COMPARISON ==========\n")
    print(df.to_string(index=False))

    return df


def plot_comparison(df):

    # Execution Time Chart
    plt.figure(figsize=(9, 5))
    plt.bar(df["Algorithm"], df["Execution Time (ms)"])
    plt.title("Algorithm Execution Time Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Execution Time (ms)")
    plt.tight_layout()
    plt.show()

    # Visited Nodes Chart
    plt.figure(figsize=(9, 5))
    plt.bar(df["Algorithm"], df["Visited Nodes"])
    plt.title("Visited Nodes Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Number of Visited Nodes")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    comparison_df = compare_algorithms()
    plot_comparison(comparison_df)
