
# ============================================================
# SMART CAMPUS NAVIGATION & EMERGENCY EVACUATION SYSTEM
# Module: Graph Construction and Management
# ============================================================

import networkx as nx

from data.campus_data import CAMPUS_LOCATIONS, CAMPUS_PATHWAYS

# ------------------------------------------------------------
# 1. CREATE CAMPUS GRAPH
# ------------------------------------------------------------

def create_campus_graph():

    graph = nx.Graph()

    # Add campus locations as nodes
    for location_id, details in CAMPUS_LOCATIONS.items():

        graph.add_node(
            location_id,
            name=details["name"],
            type=details["type"],
            x=details["x"],
            y=details["y"]
        )

    # Add pathways as weighted edges
    for source, destination, distance in CAMPUS_PATHWAYS:

        graph.add_edge(
            source,
            destination,
            distance=distance,
            blocked=False
        )

    return graph


# ------------------------------------------------------------
# 2. GET CONNECTED LOCATIONS
# ------------------------------------------------------------

def get_neighbors(graph, location):

    if location not in graph:
        return []

    neighbors = []

    for neighbor in graph.neighbors(location):

        edge_data = graph[location][neighbor]

        if not edge_data["blocked"]:

            neighbors.append((
                neighbor,
                edge_data["distance"]
            ))

    return neighbors


# ------------------------------------------------------------
# 3. CALCULATE TOTAL PATH DISTANCE
# ------------------------------------------------------------

def get_path_distance(graph, path):

    total_distance = 0

    if not path or len(path) < 2:
        return 0

    for i in range(len(path) - 1):

        source = path[i]
        destination = path[i + 1]

        if not graph.has_edge(source, destination):
            raise ValueError(
                f"No pathway exists between {source} and {destination}"
            )

        edge_data = graph[source][destination]

        if edge_data["blocked"]:
            raise ValueError(
                f"Path between {source} and {destination} is blocked"
            )

        total_distance += edge_data["distance"]

    return total_distance


# ------------------------------------------------------------
# 4. BLOCK A PATH DURING EMERGENCY
# ------------------------------------------------------------

def block_path(graph, source, destination):

    if not graph.has_edge(source, destination):
        return False

    graph[source][destination]["blocked"] = True

    return True


# ------------------------------------------------------------
# 5. RESTORE A BLOCKED PATH
# ------------------------------------------------------------

def restore_path(graph, source, destination):

    if not graph.has_edge(source, destination):
        return False

    graph[source][destination]["blocked"] = False

    return True


# ------------------------------------------------------------
# 6. GET ACTIVE GRAPH
# ------------------------------------------------------------

def get_active_graph(graph):

    active_graph = graph.copy()

    blocked_edges = [
        (u, v)
        for u, v, data in active_graph.edges(data=True)
        if data["blocked"]
    ]

    active_graph.remove_edges_from(blocked_edges)

    return active_graph


# ------------------------------------------------------------
# 7. GRAPH STATISTICS
# ------------------------------------------------------------

def get_graph_statistics(graph):

    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()

    blocked_edges = sum(
        1 for _, _, data in graph.edges(data=True)
        if data["blocked"]
    )

    active_edges = total_edges - blocked_edges

    active_graph = get_active_graph(graph)

    return {
        "total_locations": total_nodes,
        "total_pathways": total_edges,
        "active_pathways": active_edges,
        "blocked_pathways": blocked_edges,
        "connected_components": nx.number_connected_components(
            active_graph
        )
    }


# ------------------------------------------------------------
# 8. TEST GRAPH MODULE
# ------------------------------------------------------------

if __name__ == "__main__":

    campus_graph = create_campus_graph()

    print("\nSMART CAMPUS GRAPH ENGINE")
    print("=" * 40)

    print("Total Locations:", campus_graph.number_of_nodes())
    print("Total Pathways:", campus_graph.number_of_edges())

    print("\nConnected Locations from ADMIN:")

    for neighbor, distance in get_neighbors(
        campus_graph, "ADMIN"
    ):
        print(neighbor, "-", distance, "meters")

    # Test distance calculation
    test_path = ["MAIN_GATE", "ADMIN", "BLOCK_A"]

    distance = get_path_distance(
        campus_graph, test_path
    )

    print("\nTest Route:", " -> ".join(test_path))
    print("Total Distance:", distance, "meters")

    # Test emergency path blocking
    print("\nTesting Emergency Path Blocking:")

    result = block_path(
        campus_graph, "MAIN_GATE", "ADMIN"
    )

    print("Path Blocked:", result)

    print(
        "Active Neighbors of MAIN_GATE:",
        get_neighbors(campus_graph, "MAIN_GATE")
    )

    # Test path restoration
    print("\nTesting Path Restoration:")

    result = restore_path(
        campus_graph, "MAIN_GATE", "ADMIN"
    )

    print("Path Restored:", result)

    # Display statistics
    print("\nGRAPH STATISTICS")
    print("-" * 40)

    statistics = get_graph_statistics(campus_graph)

    for key, value in statistics.items():
        print(f"{key}: {value}")
