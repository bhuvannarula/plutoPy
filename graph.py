import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections
from time import sleep
import random
from demo3 import *

X,Y,Z=0,1,2
class XYZ:
    def __init__(self) -> None:
        self.X = 0
        self.Y = 0
        self.Z = 0
    def __repr__(self) -> str:
        return str((self.X, self.Y, self.Z))

class graph:
    def __init__(self, aruco : plutoArUcO) -> None:
        self.graphdelay = 1
        self.state = aruco
        self.debug = 0
        LEN = 20
        self.err_x = [0]*LEN
        self.err_y = [0]*LEN
        self.vel_x = [0]*LEN
        self.vel_y = [0]*LEN
    def animate(self):
        self.fig = plt.figure(figsize=(12,6),facecolor='#DEDEDE')
        self.ax = plt.subplot(121)
        self.ax.set_facecolor('#DEDEDE')
        # animate
        self.ani = FuncAnimation(self.fig, self.arucoGraph, interval=100)
        plt.show()

    def arucoGraph(self, i):
        #self.fix_state = XYZ()
        #self._tt = {X:random.random()*100,Y:random.random()*100,Z:random.random()*100}
        self._tt = [
            self.state._err[0],
            self.state._err[1],
            self.state.trims[0],
            self.state.trims[1]
        ]
        '''
        self._err = [
            self._tt[X],
            self._tt[Y],
            self._tt[Z]
        ]
        '''
        self.err_x.pop(0)
        self.err_x.append(self._tt[0])
        self.err_y.pop(0)
        self.err_y.append(self._tt[1])
        self.vel_x.pop(0)
        self.vel_x.append(self._tt[2])
        self.vel_y.pop(0)
        self.vel_y.append(self._tt[3])
        self.ax.cla()
        self.ax.plot(self.err_x)
        self.ax.scatter(len(self.err_x)-1, self.err_x[-1])
        self.ax.text(len(self.err_x)-1, self.err_x[-1]+2, "{}%".format(self.err_x[-1]))
        #self.ax.set_ylim(0,100)
        self.ax.plot(self.err_y)
        self.ax.scatter(len(self.err_y)-1, self.err_y[-1])
        self.ax.text(len(self.err_y)-1, self.err_y[-1]+2, "{}%".format(self.err_y[-1]))
        #self.ax.set_ylim(0,100)
        self.ax.plot(self.vel_x)
        self.ax.scatter(len(self.vel_x)-1, self.vel_x[-1])
        self.ax.text(len(self.vel_x)-1, self.vel_x[-1]+2, "{}%".format(self.vel_x[-1]))
        #self.ax.set_ylim(0,100)
        self.ax.plot(self.vel_y)
        self.ax.scatter(len(self.vel_y)-1, self.vel_y[-1])
        self.ax.text(len(self.vel_y)-1, self.vel_y[-1]+2, "{}%".format(self.vel_y[-1]))
        #self.ax.set_ylim(0,100) 


drone = plutoDrone()

pluto = plutoArUcO(drone)
pluto.debug = True
pluto.start()

sleep(13)
visual = graph(pluto)
visual.animate() 