import csv
import os

class GameDataExporter:
    def __init__(self, data):
        self.data = data

    def export_to_csv(self, filename="game_data.csv"):
        fieldnames = ["name", "round", "success_defeat", "health_remain", "win_in", "score"]
        write_header = not os.path.exists(filename)

        round_data = {}
        for key in ['success_defeat', 'health_remain', 'win_in', 'score']:
            for pair in self.data.get(key, []):
                if len(pair) != 2:
                    continue  # Skip invalid entries
                round_num, value = pair
                if round_num not in round_data:
                    round_data[round_num] = {"round": round_num}
                round_data[round_num][key] = value  # Should be int or float

        for round_num in round_data:
            round_data[round_num]["name"] = self.data.get("name", "unknown")

        with open(filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerows(round_data.values())



