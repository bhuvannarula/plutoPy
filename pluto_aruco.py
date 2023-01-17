from plutopy.aruco.plutoCV import *
from plutopy.aruco.plutoPID import *
from plutopy import plutoDrone

import threading

class XYZ:
    def __init__(self) -> None:
        self.X = 0
        self.Y = 0
        self.Z = 0
    def __repr__(self) -> str:
        return str((self.X, self.Y, self.Z))
    def reset(self):
        self.X = 0
        self.Y = 0
        self.Z = 0

class plutoArUco:
    def __init__(self, drone : plutoDrone) -> None:
        self.PIDdelay = 0.001
        self.drone = drone

        self.state = arucoState()
        self.target = XYZ()
        self.origin = XYZ()

        self.trims = []
        self._err = []

        self._threadsRunning = True
        self.debug = 0
        self._threads = []

        self.aruco = arucoGPS(self.state)

    def arucoCVThread(self):
        while self._threadsRunning:
            _err = aruco.loop()
            if _err:
                self._threadsRunning = False
                self.stop()
                break

    def setOrigin(self, iter_n : int = 10):
        '''
        Reading first 'iter_n' values & averaging to find origin, ground
        '''
        self.origin.reset()
        for _i  in range(iter_n):
            sleep(self.PIDdelay)
            _tt = self.state.X
            self.origin.X += _tt[X]
            self.origin.Y += _tt[Y]
            self.origin.Z += _tt[Z]
        self.origin.X = int(self.origin.X/iter_n)
        self.origin.Y = int(self.origin.Y/iter_n)
        self.origin.Z = int(self.origin.Z/iter_n)

    def setTarget(self, X, Y, Z):
        if (self.origin.Z == 0):
            # origin is unset
            print('Origin is not set. Target not updated.')
        else:
            self.target.X = X
            self.target.Y = Y
            self.target.Z = (self.origin.Z - Z)

    def arucoPIDThread(self):
        # Initializing PID class
        self.positionPID = positionPID()

        while self._threadsRunning:
            sleep(self.PIDdelay)
            _tt = self.state.X
            _err = [
                self.target.X - _tt[X],
                self.target.Y - _tt[Y],
                self.target.Z - _tt[Z]
            ]
            if self.debug: print("Pos Err:", _err)
            
            pitch, roll, throttle = self.positionPID.output(_err, self.state)
            pitch = constrain(pitch, -80, 80)
            roll = constrain(roll, -80, 80)
            throttle = constrain(throttle, -300, 300)

            if self.debug: print("Trim Val:", roll, pitch, throttle)
            self.trims = [pitch, roll, throttle]
            self._err = _err

            self.drone.activeState.rcRoll = 1500 + int(roll)
            self.drone.activeState.rcPitch = 1500 + int(pitch)
            self.drone.activeState.rcThrottle = 1500 + int(throttle)
        
    def start(self):
        if (self.origin.Z == 0):
            print("Warning: Origin not set!")
        procs = [self.arucoCVThread, self.arucoPIDThread]
        self._threads = []
        self._threadsRunning = True
        for proc in procs:
            _thread = threading.Thread(target=proc)
            _thread.start()
            self._threads.append(_thread)
    
    def stop_rest(self):
        self._threadsRunning = False
        for _th in self._threads[1:]:
            _th.join()
        self.drone.control.kill()
        self.drone.disconnect()

    def stop(self):
        self._threadsRunning = False
        for _th in self._threads:
            _th.join()
        self.drone.control.kill()
        self.drone.disconnect()


if __name__ == '__main__':
    drone = plutoDrone('192.168.4.1')
    drone.activeState.rcAUX3 = 2000
    drone.reconnect()
    drone.start()
    drone.reconnect()


    pluto = plutoArUco(drone)
    #pluto.debug = True
    pluto.start()

    sleep(13)
    drone.control.take_off()
    drone.activeState.rcThrottle = 1600
    sleep(1)
    drone.activeState.commandType = 0
    #drone.control.kill()
    #pluto.drone.disconnect()