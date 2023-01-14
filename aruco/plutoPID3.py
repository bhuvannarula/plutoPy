from .common import *

class positionPID:
    def __init__(self) -> None:
        self.DOF = 2
        self.position_err = [0]*self.DOF

        self.now_time = nowtime()
        self.old_time = self.now_time
        self.unit = 1e9

        self.pPOS = [0]*self.DOF
        self.iPOS = [0]*self.DOF
        self.dPOS = [0]*self.DOF

        self.pPOS[X] = 0.3
        self.iPOS[X] = 0
        self.dPOS[X] = 0

        self.pPOS[Y] = 0.3
        self.iPOS[Y] = 0
        self.dPOS[Y] = 0

        self.pVEL = [0]*self.DOF
        self.iVEL = [0]*self.DOF
        self.dVEL = [0]*self.DOF

        self.pVEL[X] = 0.3
        self.iVEL[X] = 0.1
        self.dVEL[X] = 0.8

        self.pVEL[Y] = 0.3
        self.iVEL[Y] = 0.1
        self.dVEL[Y] = 0.8

        self.iTerm = [0]*2
        self.last_vel = [0]*2

    def output(self, pos_err : list, state : arucoState):
        self.position_err[X] = pos_err[X]
        self.position_err[Y] = pos_err[Y]

        # X, Y -> P Controller
        #alt_err[X] = constrain(alt_err[X], -100, 100) # Error Reduced to 100px
        #alt_err[Y] = constrain(alt_err[Y], -100, 100) # Error Reduced to 100px

        setVel_X = constrain(self.pPOS[X] * pos_err[X], -200, 200) # Vel Max : 200px/s
        setVel_Y = constrain(self.pPOS[Y] * pos_err[Y], -200, 200) # Vel Max : 200px/s

        # Calculating Velocity
        dt = (state.now - state.old)
        if not dt:
            return 0, 0
        _newX = state.X
        _oldX = state.X_old
        vel_X = self.unit*(_newX[X] - _oldX[X])/dt
        vel_Y = self.unit*(_newX[Y] - _oldX[Y])/dt

        # Velocity -> PID Controller
        vel_err = [0]*2
        vel_err[X] = setVel_X - vel_X
        vel_err[Y] = setVel_Y - vel_Y

        # Calculating the P-Term
        result_X = constrain(self.pVEL[X] * vel_err[X], -100, 100)
        result_Y = constrain(self.pVEL[Y] * vel_err[Y], -100, 100)

        # Calculating the I-Term
        self.iTerm[X] += (self.iVEL[X] * vel_err[X]) * dt / self.unit
        self.iTerm[Y] += (self.iVEL[Y] * vel_err[Y]) * dt / self.unit

        self.iTerm[X] = constrain(self.iTerm[X], -50, 50)
        self.iTerm[Y] = constrain(self.iTerm[Y], -50, 50)

        result_X += self.iTerm[X]
        result_Y += self.iTerm[Y]

        # Calculating the D-Term
        result_X += constrain(self.dVEL[X] * (self.last_vel[X] - vel_X) * self.unit / dt, -100, 100)
        result_Y += constrain(self.dVEL[Y] * (self.last_vel[Y] - vel_Y) * self.unit / dt, -100, 100)

        return (result_X, result_Y)




