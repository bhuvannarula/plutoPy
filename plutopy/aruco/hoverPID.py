from .common import *

class calibPID:
    def __init__(self, state : arucoState) -> None:
        self.px = 0
        self.py = 0
        self.pz = 0
        self.state = state

        self.thresh = 0

    def start(self, drone):
        sleep(0.1)
        print('Starting Accn Trim Calibration!')
        t_vel = self.state.velocity()
        i, max_i = 0, 50
        while (abs(t_vel[X]) > self.thresh or i < max_i):
            trim_pitch = -int(t_vel[X]*self.px)
            trim_roll = -int(t_vel[Y]*self.py)
            drone.control.trimRollPitch(trim_roll, trim_pitch)
            sleep(0.1)




