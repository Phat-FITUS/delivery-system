class Position:
    def __init__(self, x, y, value=0, fuel=0):
        self.pos = (x, y)
        # Value is time
        self.value = value
        self.fuel = fuel

MoveDirection = {
    "up": [0, 1],
    "down": [0, -1],
    "left": [-1, 0],
    "right": [1, 0],
}