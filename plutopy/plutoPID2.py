from .plutostate import *
from .common import *
from .plutoprofile import *

from time import perf_counter_ns as nowtime

class sysTimer:
    def __init__(self) -> None:
        self._offset = nowtime()
        self.unit = 1e-9
    def get(self):
        return (nowtime() - self._offset)

'''
PID is required for 3 directions
X, Y -> For moving to coordinates / moving on correct path
Z -> Maintaining the current altitude
'''

class autofilter:
    def __init__(self, K = 5, scale_factor = 1) -> None:
        self.buffer = []
        self.K = K
        self.sf = scale_factor
    
    def __call__(self, y : int) -> int:
        self.buffer.append(y*self.sf)
        _t = len(self.buffer)
        if (_t < self.K):
            return 0
        elif (_t > self.K):
            self.buffer.pop(0)
        _t_out = int(sum(self.buffer)/self.K)/self.sf
        return _t_out

class autoDeadBand:
    def __init__(self) -> None:
        pass

X, Y, Z, = 0, 1, 2
DOF = 3

class arucoPluto:
    def __init__(self) -> None:
        self.filter = autofilter

        self.POS = [0]*DOF
        self.VEL = [0]*DOF
        self.ACC = [0]*DOF

        # Filter for raw position data
        self.POSf = [0]*DOF
        self.POSf[X] = self.filter()
        self.POSf[Y] = self.filter()
        self.POSf[Z] = self.filter()

        # Since Velocity is derived, no filter is required
        self.VELf = [0]*DOF
        self.VELf[X] = self.filter()
        self.VELf[Y] = self.filter()
        self.VELf[Z] = self.filter()

        # Filter for raw acceleration data
        self.ACCf = [0]*DOF
        self.ACCf[X] = self.filter()
        self.ACCf[Y] = self.filter()
        self.ACCf[Z] = self.filter()
    
    def setVel(self, pos : "list[3]"):
        oldPOS = list(self.POS)

        self.POS[X] = self.POSf[X](pos[X])
        self.POS[Y] = self.POSf[Y](pos[Y])
        self.POS[Z] = self.


class plutoPID:
    def __init__(self, aruco : arucoPluto) -> None:
        self.timer = sysTimer()

        self.P = [0] * DOF
        self.I = [0] * DOF
        self.D = [0] * DOF

        self.now_time = nowtime()
        self.old_time = self.now_time

        self.Pterm = [0] * DOF
        self.Iterm = [0] * DOF
        self.Dterm = [0] * DOF

        self.aruco = aruco

        '''
        X -> PID -> Pitch Increases / Decreases
        Y -> PID -> Roll Increases / Decreases
        Z -> PID -> Throttle Increases / Decreases
        '''

    def default(self):
        self.P[X] = 0
        self.I[X] = 0
        self.D[X] = 0

        self.P[Y] = 0
        self.I[Y] = 0
        self.D[Y] = 0

        self.P[Z] = 0
        self.I[Z] = 0
        self.D[Z] = 0





class plutoPID2:
    def __init__(self) -> None:
        self.timer = sysTimer()

        # PID Parameters
        self.kp = 0
        self.ki = 0
        self.kd = 0

        # Time Values
        self.now_time = nowtime()
        self.old_time = self.now_time

        # PID Terms
        self.pTerm = 0
        self.iTerm = 0
        self.dTerm = 0

        self.setPoint = 0

        self.outValue = 0

        self.last_error = 0

        self.last_y = 0

        self.windupMax = 0

        self.sampleTime = 0.2

    def output(self, y_measured):
        error = self.setPoint - y_measured

        self.now_time = nowtime()
        dt = self.now_time - self.old_time

        if (dt > self.sampleTime):
            self.pTerm = self.kp * error
            self.iTerm += self.ki * error * dt
            self.dTerm = self.kd * (self.last_y - y_measured) / dt
            
            self.antiWindUp()

            self.last_error = error
            self.old_time = self.now_time
            self.last_y = y_measured

            self.outValue = self.pTerm + self.iTerm + self.dTerm

            return self.outValue
        
        else:
            return 0
    
    def antiWindUp(self):
        if self.windupMax != 0:
            if self.iTerm > self.windupMax:
                self.iTerm = self.windupMax
            elif self.iTerm < -self.windupMax:
                self.iTerm = -self.windupMax