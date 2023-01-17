from .common import *

class positionPID:
    def __init__(self) -> None:
        self.position_err = [0]*3

        self.now_time = nowtime()
        self.old_time = self.now_time
        self.unit = 1e9

        self.pPOS = [0]*3
        self.iPOS = [0]*3
        self.dPOS = [0]*3

        self.pPOS[X] = 0.8
        self.iPOS[X] = 0#.000005
        self.dPOS[X] = 0.2

        self.pPOS[Y] = 0.8
        self.iPOS[Y] = 0#.000005
        self.dPOS[Y] = 0.2

        self.pPOS[Z] = 0.2
        self.iPOS[Z] = 0.05
        self.dPOS[Z] = 1

        self.iTerm = [0]*3
        self.last_vel = [0]*3
        self.lastP=[0]*3
        self.lastI=[0]*3
        self.lastD=[0]*3
        self.last_result = [0]*3

    def output(self, pos_err : list, state : arucoState):
        self.position_err[X] = pos_err[X]
        self.position_err[Y] = pos_err[Y]
        self.position_err[Z] = pos_err[Z]

        # X, Y, Z -> P Controller
        #setVel_X = constrain(self.pPOS[X] * pos_err[X], -500, 500) # Vel Max : 200px/s
        #setVel_Y = constrain(self.pPOS[Y] * pos_err[Y], -500, 500) # Vel Max : 200px/s
        #setVel_Z = constrain(self.pPOS[Z] * pos_err[Z], -100, 100) # Vel Max : 100cm/s

        # Calculating Velocity
        dt = (state.now - state.old)
        if not dt:
            return self.last_result
        _newX = state.X
        _oldX = state.X_old
        vel_X = self.unit*(_newX[X] - _oldX[X])/dt
        vel_Y = self.unit*(_newX[Y] - _oldX[Y])/dt
        vel_Z = self.unit*(_newX[Z] - _oldX[Z])/dt

        # Calculating the P-Term
        result_X = constrain(self.pPOS[X] * pos_err[X], -500, 500)
        result_Y = constrain(self.pPOS[Y] * pos_err[Y], -500, 500)
        result_Z = constrain(self.pPOS[Z] * pos_err[Z], -500, 500)
        p_x = constrain(self.pPOS[X] * pos_err[X], -500, 500)
        p_y = constrain(self.pPOS[Y] * pos_err[Y], -500, 500)
        p_z = constrain(self.pPOS[Z] * pos_err[Z], -500, 500)
        # Calculating the I-Term
        self.iTerm[X] += (self.iPOS[X] * pos_err[X]) * dt / self.unit
        self.iTerm[Y] += (self.iPOS[Y] * pos_err[Y]) * dt / self.unit
        self.iTerm[Z] += (self.iPOS[Z] * pos_err[Z]) * dt / self.unit
        

        self.iTerm[X] = constrain(self.iTerm[X], -50, 50)
        self.iTerm[Y] = constrain(self.iTerm[Y], -50, 50)
        self.iTerm[Z] = constrain(self.iTerm[Z], -400, 400)

        result_X += self.iTerm[X]
        result_Y += self.iTerm[Y]
        result_Z += self.iTerm[Z]
        i_x=self.iTerm[X]
        i_y=self.iTerm[Y]
        i_z=self.iTerm[Z]
        # Calculating the D-Term
        result_X += constrain(self.dPOS[X] * (vel_X) * (-1), -500, 500)
        result_Y += constrain(self.dPOS[Y] * (vel_Y) * (-1), -500, 500)
        result_Z += constrain(self.dPOS[Z] * (vel_Z) * (-1), -500, 500)
        d_x= constrain(self.dPOS[X] * (vel_X) * (-1), -500, 500)
        d_y= constrain(self.dPOS[Y] * (vel_Y) * (-1), -500, 500)
        d_z= constrain(self.dPOS[Z] * (vel_Z) * (-1), -500, 500)

        self.lastP = [p_x,p_y,p_z]
        self.lastI = [i_x,i_y,i_z]
        self.lastD = [d_x,d_y,d_z]

        self.last_vel = [vel_X, vel_Y, vel_Z]

        self.last_result = [result_X, result_Y, result_Z]

        return (result_X, result_Y, result_Z)