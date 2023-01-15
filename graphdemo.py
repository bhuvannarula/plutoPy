import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections
from time import sleep
import random
X,Y,Z=0,1,2
class XYZ:
    def __init__(self) -> None:
        self.X = 0
        self.Y = 0
        self.Z = 0
    def __repr__(self) -> str:
        return str((self.X, self.Y, self.Z))

class graph:
    def __init__(self) -> None:
        self.graphdelay = 1
        self._threadsRunning = True
        self.debug = 0
        self._threads = []
        self.err_x = collections.deque(np.zeros(10))
        self.err_y = collections.deque(np.zeros(10))
        self.err_z = collections.deque(np.zeros(10))
    def animate(self):
        self.fig = plt.figure(figsize=(12,6),facecolor='#DEDEDE')
        self.ax = plt.subplot(121)
        self.ax.set_facecolor('#DEDEDE')
        # animate
        self.ani = FuncAnimation(self.fig, self.arucoGraph, interval=1000)
        plt.show()

    def arucoGraph(self,i):
        self.fix_state = XYZ()
        self._tt = {X:random.random()*100,Y:random.random()*100,Z:random.random()*100}
        self._err = [
            self._tt[X],
            self._tt[Y],
            self._tt[Z]
        ]
        self.err_x.popleft()
        self.err_x.append(self._err[0])
        self.err_y.popleft()
        self.err_y.append(self._err[1])
        self.err_z.popleft()
        self.err_z.append(self._err[2]) 
        self.ax.cla()
        self.ax.plot(self.err_x)
        self.ax.scatter(len(self.err_x)-1, self.err_x[-1])
        self.ax.text(len(self.err_x)-1, self.err_x[-1]+2, "{}%".format(self.err_x[-1]))
        self.ax.set_ylim(0,100)
        self.ax.plot(self.err_y)
        self.ax.scatter(len(self.err_y)-1, self.err_y[-1])
        self.ax.text(len(self.err_y)-1, self.err_y[-1]+2, "{}%".format(self.err_y[-1]))
        self.ax.set_ylim(0,100)
        self.ax.plot(self.err_z)
        self.ax.scatter(len(self.err_z)-1, self.err_z[-1])
        self.ax.text(len(self.err_z)-1, self.err_z[-1]+2, "{}%".format(self.err_z[-1]))
        self.ax.set_ylim(0,100) 

g = graph()
g.animate() 