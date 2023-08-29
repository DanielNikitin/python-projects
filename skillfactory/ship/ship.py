class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coords = []

    def add_coord(self, coord):
        self.coords.append(coord)

    def covers_coord(self, coord):
        return coord in self.coords

    def is_sunk(self):
        return len(self.coords) == 0
