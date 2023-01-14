from time import perf_counter_ns as nowtime

X, Y, Z = 0, 1, 2

class arucoState:
    def __init__(self) -> None:
        self.X_new = [0]*3
        self.X_old = [0]*3
        self.X = [0]*3

        self.now = nowtime()
        self.old = self.now
    
    def __repr__(self) -> str:
        return str(self.X)
    
    def update(self, coord_data : list):
        self.X_new = list(coord_data)
        self.old = self.now
        self.now = nowtime()

def constrain(value : int, low: int, high : int):
    if (low < value <  high):
        return value
    elif (value <= low):
        return low
    elif (value >= high):
        return high