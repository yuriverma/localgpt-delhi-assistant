import json

def generate_metro_routes(json_file, output_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f:
        # --- LINES ---
        for line in data["lines"]:
            f.write(f"🚇 {line['name']} ({line['color']})\n")
            f.write(f"Route: {line['start_station']} → {line['end_station']}\n")
            stations_list = " → ".join(line["stations"])
            f.write(f"Stations ({len(line['stations'])}): {stations_list}\n")
            f.write("-" * 80 + "\n")

        # --- STATIONS ---
        f.write("\n📍 Stations\n")
        for station in data["stations"]:
            lines = ", ".join(station["lines"])
            interchange = "[Interchange]" if station["is_interchange"] else "[Normal]"
            f.write(f"- {station['name']} (Lines: {lines}) {interchange}\n")

        # --- CONNECTIONS ---
        f.write("\n🔗 Connections\n")
        for conn in data["connections"]:
            f.write(f"- {conn['from']} ⇄ {conn['to']} [{conn['line']}, {conn['travel_time_minutes']} min]\n")

    print(f"✅ Metro routes exported to {output_file}")


if __name__ == "__main__":
    generate_metro_routes("data/delhi_metro.json", "data/metro_routes.txt")

