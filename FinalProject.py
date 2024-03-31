import csv
import heapq

# Initialize an empty graph
graph = {}

# Read the CSV file that is present in the same directory
with open('graph_edges.csv', mode='r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        source, target, weight = row
        weight = int(weight)  # This will convert the weight to an integer
        if source not in graph:
            graph[source] = {}
        graph[source][target] = weight
        if target not in graph:
            graph[target] = {}
        graph[target][source] = weight  # Add the edge in both directions 

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances, previous_nodes

def reconstruct_path(previous_nodes, start, end):
    path = []
    current_node = end
    while current_node and current_node != start:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.append(start)
    path.reverse()
    return path

# Asking for the starting node from the user
start_node = input("Enter the starting node: ")  # Dynamically set the starting point
charging_stations = ['H', 'K', 'Q', 'T']
distances, previous_nodes = dijkstra(graph, start_node)

# Finding and displaying the shortest paths to each charging station
for station in charging_stations:
    path = reconstruct_path(previous_nodes, start_node, station)
    print(f"Shortest path to {station} charging station: {path}")

# Route Recommendation System
# Finding the nearest charging station by comparing distances
nearest_station = min(charging_stations, key=lambda station: distances[station])
recommended_path = reconstruct_path(previous_nodes, start_node, nearest_station)

print(f"\nThe recommended shortest path to the nearest charging station which is [{nearest_station}] is: {recommended_path}")
