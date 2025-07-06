import pandas as pd
from collections import defaultdict, deque
import time

# Load GTFS files
stops = pd.read_csv("data/metro_gtfs/stops.txt")
stop_times = pd.read_csv("data/metro_gtfs/stop_times.txt")
trips = pd.read_csv("data/metro_gtfs/trips.txt")
routes = pd.read_csv("data/metro_gtfs/routes.txt")

# Create stop_id → stop_name mapping
stop_id_to_name = dict(zip(stops.stop_id, stops.stop_name))
stop_name_to_id = dict(zip(stops.stop_name, stops.stop_id))

# Create trip_id → route_id mapping
trip_to_route = dict(zip(trips.trip_id, trips.route_id))

# Create route_id → route_name mapping
route_to_name = dict(zip(routes.route_id, routes.route_long_name))

# Build graph (station_name → [(connected_station_name, line_name)])
graph = defaultdict(list)
ordered_times = stop_times.sort_values(by=["trip_id", "stop_sequence"])

for trip_id, group in ordered_times.groupby("trip_id"):
    route_id = trip_to_route.get(trip_id, "")
    line_name = route_to_name.get(route_id, "Unknown Line")
    stop_sequence = list(group.stop_id)

    for i in range(len(stop_sequence) - 1):
        from_stop = stop_id_to_name.get(stop_sequence[i], "")
        to_stop = stop_id_to_name.get(stop_sequence[i + 1], "")
        if from_stop and to_stop:
            graph[from_stop].append((to_stop, line_name))
            graph[to_stop].append((from_stop, line_name))  # bidirectional

# Shortest path finder (BFS)
def find_shortest_path(src, dest):
    visited = set()
    queue = deque([(src, [src], [])])  # (current_node, path, lines)

    while queue:
        node, path, lines = queue.popleft()
        if node == dest:
            return path, lines
        if node in visited:
            continue
        visited.add(node)
        for neighbor, line in graph.get(node, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], lines + [line]))
    return None, None

# Output file
output_file = "data/metro_routes.txt"
seen = set()
count = 0
MAX_PAIRS = 1000  # cap for dev mode

stations = list(stop_name_to_id.keys())

with open(output_file, "w") as f:
    total = len(stations)**2
    for src in stations:
        for dest in stations:
            if src == dest or (src, dest) in seen or (dest, src) in seen:
                continue
            seen.add((src, dest))

            count += 1
            if count % 50 == 0:
                print(f"🛠️  Processing {count} pairs: {src} → {dest}")

            # Set timeout
            start = time.time()
            path, lines = find_shortest_path(src, dest)
            duration = time.time() - start

            if duration > 3:
                print(f"⏳ Skipped slow route {src} → {dest} ({int(duration)}s)")
                continue

            if path and lines:
                route_line = f"{src} to {dest} via {' → '.join(path)} | Lines: {' → '.join(lines)}"
                f.write(route_line + "\n")

            if count >= MAX_PAIRS:
                print("✅ Reached max dev limit.")
                break

print(f"✅ Done. Output saved to {output_file}")

