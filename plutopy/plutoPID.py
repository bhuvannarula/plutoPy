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

barometerConfig = None
pidProfile = None
rcControlsConfig = None
barometerConfig_t = None

QUEUE_MAX_LENGTH = 15

buff = [0]*15
head = 0
rear = -1
itemCount = 0
_time_constant_z = 2.0
accZ_tmp = None
accZ_old = None

first_reads = 0
first_velocity_reads = 0

BARO_UPDATE_FREQUENCY_40HZ = 1000*25
UPDATE_FREQUENCY = 1000*10

DEGREES_80_IN_DECIDEGREES = 800
ROLLOVER_DEGREES = 80

# TODO
#EstAlt = 0
# EstAlt is nothing but the current height of drone
#AltHold = 10 # Target Altitude

# TODO
armingFlags = 0
ARMED = 4
def ARMING_FLAG(state : int):
    # TODO
    return (armingFlags & (state))

'''
Depricated, moved to plutoprofile.py
class profilePID:
    def __init__(self) -> None:
        self.P8 = [0]*PID_ITEM_COUNT
        self.I8 = [0]*PID_ITEM_COUNT
        self.D8 = [0]*PID_ITEM_COUNT

        self.P8[PIDROLL] = 40
        self.I8[PIDROLL] = 10
        self.D8[PIDROLL] = 30
        self.P8[PIDPITCH] = 40
        self.I8[PIDPITCH] = 10
        self.D8[PIDPITCH] = 30
        self.P8[PIDYAW] = 150
        self.I8[PIDYAW] = 70
        self.D8[PIDYAW] = 50
        self.P8[PIDALT] = 100
        self.I8[PIDALT] = 0
        self.D8[PIDALT] = 30
        self.P8[PIDVEL] = 120
        self.I8[PIDVEL] = 45
        self.D8[PIDVEL] = 1
        self.P8[PIDUSER] = 0
        self.I8[PIDUSER] = 0
        self.D8[PIDUSER] = 0   
'''

class arucoAlt:
    def __init__(self) -> None:
        self.alt = 0
        self.alt_offset = 0
        self.last_alt = 0

class arucoConfig:
    def __init__(self) -> None:
        '''
        Values borrowed from barometerConfig
        '''
        self.sample_count = 21
        self.noise_lpf = 0.6
        #self.cf_vel = 0.985
        #self.cf_alt = 0.92
        self.cf_vel = 1
        self.cf_alt = 1

class altitudePID:
    def __init__(self, pose : plutoState, PIDconfig : profilePID): #, Alt : arucoAlt) -> None:
        self.velocityControl = 1
        self.maxAltitude = -1
        self.altholdThrottle = 0
        self.errorVelocityI = 0
        self.altholdThrottleAdjustment = 0
        self.althold1 = None
        self.vario = 0
        self.setVelocity = 0
        self.calculatedError = 10
        self.velocityZ = None
        self.positionZ = None
        self.altRstRequired = 1
        
        self.pose = pose
        self.PID = PIDconfig
        self.aruco = arucoAlt() #Alt
        self.config = arucoConfig()
        self.timer = sysTimer()

        self.AltHold = 0
        self.EstAlt = 0

        self.previousTime = 0
        
        self.baroAlt_offset_print = 0
        self.velControlDebug = [0]*3

        self.accZ_tmp = 0
        self.accZ_old = 0
        self.vel = 0
        self.accAlt = 0

        self.previousTimeZ = 0
        self.altHoldThrottleAdjustment = 0

        self.acc_1G = 512 # 256
        self.accVelScale = 9.80665 / self.acc_1G * 100

        self._ti = 0

    def isThrustFacingDownwards(self):
        return (abs(self.pose.rcRoll) < ROLLOVER_DEGREES) and (abs(self.pose.rcPitch) < ROLLOVER_DEGREES)

    def calculateAltHoldThrottleAdjustment(self, velocity_z : int, accZ_tmp : float, accZ_old : float):
        result = 0

        if (not self.isThrustFacingDownwards()):
            return result

        # Altitude P-Controller
        if (not ARMING_FLAG(ARMED)):
            self.AltHold = self.EstAlt

        if (not self.velocityControl):
            error = constrain(self.AltHold - self.EstAlt, -500, 500)
            error = applyDeadband(error, 5)
        
            setVel = constrain(int((self.PID.P8[PIDALT] * error) / 128), -300, 300) # Limit Velocity to +/- 3m/s
        else:
            setVel = self.setVelocity

        # Velocity PID-Controller

        # P
        error = setVel - velocity_z
        # altholdDebug9 = error
        result = constrain(int(self.PID.P8[PIDVEL] * error / 32), -300, 300)
        self.velControlDebug[0] = result

        # I
        if (ARMING_FLAG(ARMED)):
            self.errorVelocityI += (self.PID.I8[PIDVEL] * error)
        else:
            self.errorVelocityI = 0

        self.errorVelocityI = constrain(self.errorVelocityI, -(8192 * 300), (8192 * 300))
        result += int(self.errorVelocityI / 8192)
        self.velControlDebug[1] = int(self.errorVelocityI / 8192)

        # D
        errorVelocityD = constrain(int(self.PID.D8[PIDVEL] * (accZ_tmp + accZ_old) / 512), -150, 150)
        result -= errorVelocityD
        self.velControlDebug[2] = errorVelocityD

        return result


    def calculateEstimatedAltitude(self): #, currentTime : int):
        '''
        accSum, accSumCount replaced by self.pose.accZ

        currentTime replaced by time from perf_counter_ns
        '''
        currentTime = self.timer.get()

        # TODO variables:
        accTimeSum = 0
        accSumCount = 0
        accSum = [0]*3

        self.dTime = currentTime - self.previousTime
        '''
        if (dTime < BARO_UPDATE_FREQUENCY_40HZ):
            return None
        '''

        self.previousTime = currentTime

        # TODO : wait for aruco calibration

        self.aruco.alt -= self.aruco.alt_offset

        # Integrator - Velocity, cm/sec
        #dt = float(accTimeSum * 1e-6)
        dt = float(self.dTime * self.timer.unit)
        if (self._ti < 100):
            self._ti += 1
            return
        if (dt < 0.1):
            self.accZ_tmp = applyDeadRegion(self.pose.accZ - self.acc_1G, 2)
        else:
            self.accZ_tmp = 0
        
        self.debug0 = (self.accZ_tmp, self.accVelScale, dt, '#0')
        self.vel_acc = self.accZ_tmp * self.accVelScale * dt
        self.debug1 = (dt, self.vel_acc, self.accAlt, self.vel, '#1')
        # Integrator - Altitude, cm
        self.accAlt += ((self.vel_acc * 0.5) * dt) + (self.vel * dt)
        accalttemp = int(100*self.accAlt)
        self.accAlt = (self.accAlt * self.config.cf_alt) + self.aruco.alt * (1 - self.config.cf_alt)
        self.vel += self.vel_acc
        self.debug2 = (self.accAlt, self.vel, '#2')
        self.arucoVel = (self.aruco.alt - self.aruco.last_alt) * dt
        self.aruco.last_alt = self.aruco.alt

        self.arucoVel = constrain(self.arucoVel, -1500, 1500) # Constrain aruco velocity to +- 1500 cm/s
        self.arucoVel = applyDeadband(self.arucoVel, 10) # to reduce noise near zero

        self.vel = self.vel * self.config.cf_vel + self.arucoVel * (1 - self.config.cf_vel)
        vel_tmp =  int(self.vel)

        if (False): # BIG TODO, loop should loop for Altitude Hold, this only when we change altitude
            self.altHoldThrottleAdjustment = self.calculateAltHoldThrottleAdjustment(vel_tmp, self.accZ_tmp, self.accZ_old)

        self.accZ_old = self.accZ_tmp

    def resetAltitude(self):
        self.vel = 0
        self.accAlt = 0