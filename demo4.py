#from plutopy.aruco.common import *
from plutopy.aruco.plutoCV import *
from plutopy.aruco.filters import deadband
from plutopy.aruco.plutoPID3 import *
from plutopy import plutoDrone
from plutopy.pluto import *
import threading

class XYZ:
    def __init__(self) -> None:
        self.X = 0
        self.Y = 0
        self.Z = 0
    def __repr__(self) -> str:
        return str((self.X, self.Y, self.Z))

class plutoArUcO:
    def __init__(self, drone : plutoDrone) -> None:
        self.PIDdelay = 0.001
        self.drone = drone

        self.state = arucoState()

        self.trims = []
        self._err = []

        self._threadsRunning = True
        self.debug = 0
        self._threads = []

        self.aruco = arucoGPS(self.state)

    def coord_dead(self):
        _t = 1
        _X = deadband(self.state.X_new[X], self.state.X_old[X], _t)
        _Y = deadband(self.state.X_new[Y], self.state.X_old[Y], _t)
        _Z = deadband(self.state.X_new[Z], self.state.X_old[Z], _t)
        _tt = [_X, _Y, _Z]
        self.state.X_old = list(self.state.X)
        self.state.X = list(_tt)
        return _tt

    def arucoCVThread(self):
        while self._threadsRunning:
            _err = self.aruco.loop()
            if _err:
                self._threadsRunning = False
                break

    def arucoPIDThread(self):
        #sleep(10)
        fix_state = XYZ()
        iter_n = 10
        for _i  in range(iter_n):
            _tt = self.coord_dead()
            fix_state.X += _tt[X]
            fix_state.Y += _tt[Y]
            fix_state.Z += _tt[Z]
        fix_state.X = int(fix_state.X/iter_n)
        fix_state.Y = int(fix_state.Y/iter_n)
        fix_state.Z = int(fix_state.Z/iter_n)

        self.positionPID = positionPID()

        while self._threadsRunning:
            sleep(self.PIDdelay)
            _tt = self.coord_dead()
            _err = [
                fix_state.X - _tt[X],
                fix_state.Y - _tt[Y],
                fix_state.Z - _tt[Z]
            ]
            if self.debug: print("Pos Err:", _err)
            
            trim_pitch, trim_roll = self.positionPID.output(_err, self.state)
            trim_pitch = constrain(trim_pitch, -80, 80)
            trim_roll = constrain(trim_roll, -80, 80)
            if self.debug: print("Trim Val:", trim_roll, trim_pitch)
            self.trims = [trim_pitch, trim_roll]
            self._err = _err

            #self.drone.activeState.rcRoll = 1500 + int(trim_roll)
            #self.drone.activeState.rcPitch = 1500 + int(trim_pitch)
        
    def start(self):
        procs = [self.arucoCVThread]#, self.arucoPIDThread]
        self._threads = []
        self._threadsRunning = True
        for proc in procs:
            _thread = threading.Thread(target=proc)
            _thread.start()
            self._threads.append(_thread)
    
    def stop(self):
        self._threadsRunning = False
        for _th in self._threads:
            _th.join()
        self.drone.control.kill()
        self.drone.disconnect()


class calibPID:
    def __init__(self, state : arucoState) -> None:
        self.px = 0
        self.py = 0
        self.pz = 0
        self.state = state

        self.debug = True

        self.thresh = 0

    def start0(self, drone : plutoDrone):
        sleep(0.1)
        print('Starting Accn Trim Calibration!')
        t_vel = self.state.velocity()
        i, max_i = 0, 50
        while (abs(t_vel[X]) > self.thresh or i < max_i):
            trim_pitch = -int(t_vel[X]*self.px)
            trim_roll = -int(t_vel[Y]*self.py)
            drone.control.trimRollPitch(trim_roll, trim_pitch)
            sleep(0.1)
            t_vel = self.state.velocity()

    def get(self):
        sleep(0.05)
        delay = 0.2
        print('Starting Accn Trim Calibration!')
        t_vel_0 = self.state.velocity()
        if self.debug: print("Vel0 :", t_vel_0)
        sleep(delay)
        t_vel_1 = self.state.velocity()
        if self.debug: print("Vel1 :", t_vel_1)
        tf = int(1/delay)
        accn = [
            (t_vel_1[X] - t_vel_0[X])*tf,
            (t_vel_1[Y] - t_vel_0[Y])*tf
        ]
        if self.debug: print("Accn :", accn)
        trim_pitch = -int(accn[X]*self.px)
        trim_roll = -int(accn[Y]*self.py)
        return (trim_roll, trim_pitch)


drone = plutoDrone()

# Setting to AltHold Mode
#drone.activeState.rcAUX3 = 2000
drone.reconnect()
drone.start()
drone.reconnect()

# Starting Camera
pluto = plutoArUcO(drone)
print("Camera Started!")
pluto.debug = True
pluto.start()

px, py = 0, 0

while True:
    drone.activeState.commandType = NONE_COMMAND
    drone.control.take_off()
    #drone.activeState.rcThrottle 
    sleep(1.5)
    drone.activeState.commandType = NONE_COMMAND
    calibrator = calibPID(pluto.state)
    calibrator.debug = True
    calibrator.px = px
    calibrator.py = py
    trim = calibrator.get()
    print(trim)
    drone.control.trimRollPitch(*trim)
    sleep(1)
    drone.control.land()

    px, py = input("Enter px, py:").split(' ')[:2]
    px = float(px)
    py = float(py)

