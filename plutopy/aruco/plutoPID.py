from .common import *

class positionPID:
    def __init__(self) -> None:
        self.position_err = [0]*3

        self.now_time = nowtime()
        self.old_time = self.now_time
        self.unit = 1e9

        self.pPOS = [0]*3

        self.pPOS[X] = 1.6
        self.pPOS[Y] = 1.6
        self.pPOS[Z] = 0

        self.pVEL = [0]*3
        self.iVEL = [0]*3
        self.dVEL = [0]*3

        self.pVEL[X] = 2.4
        self.iVEL[X] = 0
        self.dVEL[X] = 2

        self.pVEL[Y] = 2.4
        self.iVEL[Y] = 0
        self.dVEL[Y] = 2

        self.pVEL[Z] = 3
        self.iVEL[Z] = 0.4
        self.dVEL[Z] = 0

        self.iTerm = [0]*3
        self.last_vel = [0]*3

    def output(self, pos_err : list, state : arucoState):
        self.position_err[X] = pos_err[X]
        self.position_err[Y] = pos_err[Y]
        self.position_err[Z] = pos_err[Z]

        # X, Y, Z -> P Controller
        setVel_X = constrain(self.pPOS[X] * pos_err[X], -500, 500) # Vel Max : 200px/s
        setVel_Y = constrain(self.pPOS[Y] * pos_err[Y], -500, 500) # Vel Max : 200px/s
        setVel_Z = constrain(self.pPOS[Z] * pos_err[Z], -100, 100) # Vel Max : 100cm/s

        # Calculating Velocity
        dt = (state.now - state.old)
        if not dt:
            return 0, 0, 0
        _newX = state.X
        _oldX = state.X_old
        vel_X = self.unit*(_newX[X] - _oldX[X])/dt
        vel_Y = self.unit*(_newX[Y] - _oldX[Y])/dt
        vel_Z = self.unit*(_newX[Z] - _oldX[Z])/dt

        # Velocity -> PID Controller
        vel_err = [0]*3
        vel_err[X] = setVel_X - vel_X
        vel_err[Y] = setVel_Y - vel_Y
        vel_err[Z] = setVel_Z - vel_Z

        # Calculating the P-Term
        result_X = constrain(self.pVEL[X] * vel_err[X], -100, 100)
        result_Y = constrain(self.pVEL[Y] * vel_err[Y], -100, 100)
        result_Z = constrain(self.pVEL[Z] * vel_err[Z], -500, 500)
        print("P", result_Z)

        # Calculating the I-Term
        self.iTerm[X] += (self.iVEL[X] * vel_err[X]) * dt / self.unit
        self.iTerm[Y] += (self.iVEL[Y] * vel_err[Y]) * dt / self.unit
        self.iTerm[Z] += (self.iVEL[Z] * vel_err[Z]) * dt / self.unit

        self.iTerm[X] = constrain(self.iTerm[X], -50, 50)
        self.iTerm[Y] = constrain(self.iTerm[Y], -50, 50)
        self.iTerm[Z] = constrain(self.iTerm[Z], -500, 500)
        print("I", self.iTerm)

        result_X += self.iTerm[X]
        result_Y += self.iTerm[Y]
        result_Z += self.iTerm[Z]

        # Calculating the D-Term
        result_X += constrain(self.dVEL[X] * (self.last_vel[X] - vel_X) * self.unit / dt, -100, 100)
        result_Y += constrain(self.dVEL[Y] * (self.last_vel[Y] - vel_Y) * self.unit / dt, -100, 100)
        result_Z += constrain(self.dVEL[Z] * (self.last_vel[Z] - vel_Z) * self.unit / dt, -100, 100)
        print("D", result_Z)

        self.last_vel = [vel_X, vel_Y, vel_Z]

        return (result_X, result_Y, result_Z)

class altitudePID:
    def __init__(self) -> None:
        pass