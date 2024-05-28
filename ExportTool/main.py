from pathlib import Path
import json
from Model.main import Garden

class ExportTool:
    def __init__(self, save_directory: str = "../save_files"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(parents=True, exist_ok=True)

    def export(self, garden: Garden, filename: str = "garden_export.json"):
        garden_state = self.serialize_garden(garden)
        filepath = self.save_directory / filename
        with open(filepath, 'w') as file:
            json.dump(garden_state, file)

    def load(self, filename: str = "garden_export.json"):
        filepath = self.save_directory / filename
        with open(filepath, 'r') as file:
            garden_state = json.load(file)
            return garden_state

    def serialize_garden(self, garden: Garden):
        return {
            "size": garden.size,
            "tiles": [
                [
                    [
                        tile.tile_type.name for tile in stack
                    ] for stack in row
                ] for row in garden.tiles
            ]
        }
