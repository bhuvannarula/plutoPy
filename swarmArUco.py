from aruco.plutoCV import *
from aruco.plutoPID import *
from plutopy import plutoDrone, plutoSwarm
from aruco.filter import lpfilterZ
from aruco.kalman import KalmanFilter

import threading

class cameraFeed:
    def __init__(self) -> None:
        self.camera = arucoCamera()

        self.update = self.camera.update

        self._running = True
        self._thread = threading.Thread(target=self.loop)
        self._thread.start()
    
    def loop(self):
        while self._running:
            _err = self.camera.loop()
            if _err:
                self._running = False
                break
    
    def stop(self):
        self._running = False
        self._thread.join()

class plutoArUco:
    def __init__(self, camera : cameraFeed, drone : plutoDrone, droneID : int) -> None:
        self.PIDdelay = 0.001
        self.drone = drone
        self.targetID = droneID
        self.k = KalmanFilter()
        self.state = arucoState()
        self.target = XYZ()
        self.origin = XYZ()
        self.droneAngle = lowPassFilter()
        self.Zfil = lpfilterZ()
        self._err = []

        self._threadsRunning = True
        self.debug = 0
        self._threads = []

        self.procs = [self.arucoPIDThread]

        self.file = open(f'logs/dumpPID-{self.targetID}.csv', 'w', newline='\n')
        self.csv = csv.writer(self.file)

        self.camera = camera  #arucoGPS(self.state, droneID, self.droneAngle)

        self.positionPID = positionPID()

    def arucoCVThread(self):
        self.camera.update(self.state, self.targetID, self.droneAngle)

    def setOrigin(self, iter_n : int = 50):
        '''
        Reading first 'iter_n' values & averaging to find origin, ground
        '''
        origin = XYZ()
        for _i  in range(iter_n):
            sleep(self.PIDdelay)
            _tt = self.state.X
            origin.X += _tt[X]
            origin.Y += _tt[Y]
            origin.Z += _tt[Z]
            origin.A += self.droneAngle.get()
        self.origin.X = round(origin.X/iter_n, 2)
        self.origin.Y = round(origin.Y/iter_n, 2)
        self.origin.Z = int(origin.Z/iter_n)
        self.origin.A = round(origin.A/iter_n, 2)
        print("Angle of Drone {}:", self.origin.A)

        # Configuring Kalman Filter
        self.k.Configure(self.origin.Z - self.state.X[Z],0,(1-self.drone.state.accZ))

    def setTarget(self, X, Y, Z):
        if (self.origin.Z == 0):
            # origin is unset
            print(f'Origin is not set for drone {self.targetID}. Target not updated.')
        else:
            self.target.X = X
            self.target.Y = Y
            self.target.Z = Z

    def arucoPIDThread(self):
        sleep(self.PIDdelay)
        _tt = self.state.X
        self.k.Update(self.origin.Z - self.state.X[Z],self.drone.state.accZ,self.state.dt/self.state.unit)
        angle = radians(self.origin.A - 90)
        angle = radians(self.droneAngle.get() - 90)
        cosA = cos(angle)
        sinA = sin(angle)
        _eX = self.target.X - _tt[X]
        _eY = self.target.Y - _tt[Y]
        _eX = _eX * cosA + _eY * sinA
        _eY = _eY * cosA - _eX * sinA
        self.Zfil.update(self.k.z_)
        _err = [
            _eX,
            _eY,
            self.target.Z - (self.Zfil.get()),
            angle
        ]

        if self.debug: print("Pos Err:", _err)
        
        pitch, roll, throttle, = self.positionPID.output(_err, self.state)
        pitch = constrain(pitch, -400, 400)
        roll = constrain(roll, -500, 500)
        throttle = constrain(throttle, -200, 200)

        zp = self.positionPID.lastP[Z]
        zi = self.positionPID.lastI[Z]
        zd = self.positionPID.lastD[Z]
        self.csv.writerow([*_err[:3], pitch, roll, throttle, zp, zi, zd])

        if self.debug: print("Trim Val:", roll, pitch, throttle)
        
        self._err = _err

        self.drone.activeState.rcRoll = 1500 + int(roll)
        self.drone.activeState.rcPitch = 1500 + int(pitch)
        self.drone.activeState.rcThrottle = 1500 + int(throttle)
        
    def start(self):
        if (self.origin.Z == 0):
            print(f"Warning: Origin not set for drone {self.targetID}!")
        self._threadsRunning = True
        for proc in self.procs:
            _thread = threading.Thread(target=proc)
            _thread.start()
            self._threads.append(_thread)
    
    def stop_rest(self):
        self._threadsRunning = False
        for _th in self._threads[1:]:
            _th.join()
        self.file.flush()
        self.file.close()
        self.drone.control.kill()
        if self.drone._threadsRunning:
            self.drone.disconnect()

    def stop(self):
        self.drone.control.kill()
        if self.drone._threadsRunning:
            self.drone.disconnect()

class swarmArUco:
    def __init__(self, swarm : plutoSwarm, droneIDs : dict) -> None:
        '''
        droneIDs should be dict, with key as drone name, and value as ArUco Tag ID
        {droneName : ArUcoID}
        '''
        self.camera = cameraFeed()
        self.drones = swarm
        self.droneIDs = droneIDs
        self.origin = XYZ()

        self._threadsRunning = True
        self._proc = [self.cvThread]
        self._thread = []
        self.delay = 0.001

        self.aruco = {}
        for kk in self.droneIDs:
            drone = self.drones[kk]
            droneID = self.droneIDs[kk]
            self.aruco[kk] = plutoArUco(self.camera, drone, droneID)
    
    def __getitem__(self, key) -> plutoArUco:
        if key not in self.droneIDs:
            return self.__missing__(key)
        else:
            return self.aruco[key]

    def __missing__(self, key) -> None:
        print("[WARNING] No drone with ID :", key)
        return None

    def setOrigins(self):
        #self.aruco[droneID].setOrigin()
        #origin = self.aruco[droneID].origin
        for id in self.aruco:
            self.aruco[id].setOrigin()
        #self.origin = self.aruco[droneName].origin
    
    def originTarget(self, Z : float = 90):
        for id in self.aruco:
            t_X = self.aruco[id].origin.X
            t_Y = self.aruco[id].origin.Y
            t_Z = 90
            self[id].setTarget(t_X, t_Y, t_Z)

    def cvThread(self):
        print(0)
        while self._threadsRunning:
            print(1, self.camera._running)
            sleep(self.delay)
            if self.camera._running:
                print(2)
                for id in self.aruco:
                    self.aruco[id].arucoCVThread()
                    print('hello')
            else:
                self._threadsRunning = False
                self.stop_rest()
                break

    def start(self):
        thread = threading.Thread(target=self.cvThread)
        thread.start()
        self._thread.append(thread)
        for item in self.aruco:
            self.aruco[item].start()

    def stop_rest(self):
        for item in self.aruco:
            self.aruco[item].stop_rest()

    def stop(self):
        for item in self.aruco:
            self.aruco[item].stop()

    def take_off_all(self):
        for item in self.aruco:
            self.drones[item].control.take_off()

    def land_all(self):
        for item in self.aruco:
            self.drones[item].control.land()

def avg(lst : list):
    return round(sum(lst)/len(lst), 3)

def queue(lst : list, element : float):
    lst.append(element)
    lst.pop(0)

def makeSure(droneArUco : plutoArUco):
    recordX = [100]*100
    recordY = [100]*100
    recordZ = [100]*100

    aruco = droneArUco
    _err = aruco._err

    while True:
        queue(recordX, abs(_err[X]))
        queue(recordY, abs(_err[Y]))
        queue(recordZ, abs(_err[Z]))
        if (avg(recordX) < 5) and (avg(recordY) < 5) and (avg(recordZ) < 5):
            # Drone Reached Target
            return 0
        else:
            sleep(0.01)
