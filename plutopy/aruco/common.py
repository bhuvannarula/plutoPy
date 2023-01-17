from time import perf_counter_ns as nowtime
from time import sleep
from .filters import *

X, Y, Z = 0, 1, 2

class arucoState:
    def __init__(self) -> None:
        self.X_new = [0]*3
        self.X_old = [0]*3
        self.X = [0]*3

        self.now = nowtime()
        self.old = self.now

        self.i_now = 0
        self.i_old = 0

        self.unit = 1e9
    
    def __repr__(self) -> str:
        return str(self.X)
    
    def update(self, coord_data : list, i : int):
        self.X_new = list(coord_data)
        self.old = self.now
        self.now = nowtime()
        self.i_old = int(self.i_now)
        self.i_now = i
        _t = 1
        _X = deadband(self.X_new[X], self.X_old[X], _t)
        _Y = deadband(self.X_new[Y], self.X_old[Y], _t)
        _Z = deadband(self.X_new[Z], self.X_old[Z], _t)
        _tt = [_X, _Y, _Z]
        self.X_old = list(self.X)
        self.X = list(_tt)
        return _tt

    def velocity(self):
        dt = self.now-self.old
        if not dt:
            return 0, 0
        _new = self.X
        _old = self.X_old
        #vel_x = self.unit*(_new[X] - _old[X])/dt
        #vel_y = self.unit*(_new[Y] - _old[Y])/dt
        vel_x = int((_new[X] - _old[X])/(self.i_now - self.i_old))
        vel_y = int((_new[Y] - _old[Y])/(self.i_now - self.i_old))
        return (vel_x, vel_y)

def constrain(value : int, low: int, high : int):
    if (low < value <  high):
        return value
    elif (value <= low):
        return low
    elif (value >= high):
        return high