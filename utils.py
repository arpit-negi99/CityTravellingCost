import heapq

# Graph data with distances in km
graph = {
    "Clock Tower": {"FRI": 3.0, "ISBT Dehradun": 5.0, "Rajpur Road": 2.0},
    "FRI": {"Clock Tower": 3.0, "ISBT Dehradun": 3.5, "Tapkeshwar Temple": 2.5, "Dehradun Zoo": 4.0},
    "ISBT Dehradun": {"Clock Tower": 5.0, "FRI": 3.5},
    "Tapkeshwar Temple": {"FRI": 2.5, "Robbers Cave": 3.5},
    "Robbers Cave": {"Tapkeshwar Temple": 3.5, "Sahastradhara": 4.5},
    "Sahastradhara": {"Robbers Cave": 4.5, "Mussoorie Road": 6.0},
    "Mussoorie Road": {"Sahastradhara": 6.0, "Pacific Mall": 3.5, "Rajpur Road": 4.0},
    "Pacific Mall": {"Mussoorie Road": 3.5, "Dehradun Zoo": 3.0, "Rajpur Road": 2.0},
    "Dehradun Zoo": {"FRI": 4.0, "Pacific Mall": 3.0},
    "Rajpur Road": {"Clock Tower": 2.0, "Mussoorie Road": 4.0, "Pacific Mall": 2.0}
}

# Coordinates (lat, lon) for each place
coords = {
    "Clock Tower": (30.3255, 78.0437),
    "FRI": (30.3385, 77.9996),
    "ISBT Dehradun": (30.2841, 78.0126),
    "Tapkeshwar Temple": (30.3365, 77.9877),
    "Robbers Cave": (30.3695, 78.0541),
    "Sahastradhara": (30.3951, 78.1317),
    "Mussoorie Road": (30.3751, 78.0654),
    "Pacific Mall": (30.3606, 78.0676),
    "Dehradun Zoo": (30.3194, 78.0796),
    "Rajpur Road": (30.3655, 78.0782)
}

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return path, cost
        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return None, float('inf')