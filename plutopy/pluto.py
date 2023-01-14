from time import sleep
from .protocol import *
from .commands import *
from .plutoinfo import *
from .plutoPID import *
import threading

class plutoDrone():
    def __init__(self, IP_ADDRESS : str = '192.168.4.1', CAMERA_IP_ADDRESS : str = '', PORT : int = 23, CAMERA_PORT :int = 9060, debug = False) -> None:
        
        self.status = 0 # Not Running

        # False -> Threads Stop Running
        self._threadsRunning = True
        self._threads =  []

        # Step 0 : Initialize the State Instances of Drone
        self.activeState = plutoState()
        self.activeStateAP = plutoState()
        self.responseState = plutoState()
        self.PIDconfig = profilePID()

        # Step 1 : Initialize the Read Buffer for Drone
        self.buffer = plutoBuffer()

        # Step 2 : Initialize the socket for Drone
        self.sock = plutoSock(IP_ADDRESS, PORT, self.buffer, self.responseState, self.PIDconfig)
        
        # Step 3 : Connecting to Socket
        self.sock.connect()

        # Step 4 : Initialize MSP Instance
        self.MSP = plutoMSP(self.sock)

        # Attaching command controls to class
        self.control = plutoControl(self.activeState, self.MSP)

        # Attaching info commands to class
        self.info = plutoInfo(self.responseState)

        #self.PID = altitudePID(self.responseState)

        self.target_threads = [self.writeThread, self.readThread]
    
    def writeThread(self):
        requests = [MSP_RC, MSP_ATTITUDE, MSP_RAW_IMU, MSP_ALTITUDE, MSP_ANALOG]
        requests = []

        self.MSP.sendRequestMSP_ACC_TRIM()

        while (self._threadsRunning):
            state = self.activeState.array()
            if (self.activeState.isAutoPilotOn and state[7]):
                state[0] += self.activeStateAP.rcRoll - 1500
                state[1] += self.activeStateAP.rcPitch - 1500
                state[2] += self.activeStateAP.rcThrottle - 1500
                state[3] += self.activeStateAP.rcYaw - 1500
            
            self.MSP.sendRequestMSP_SET_RAW_RC(state)
            self.MSP.sendRequestMSP_GET_DEBUG(requests)

            if (self.activeState.commandType != NONE_COMMAND):
                self.MSP.sendRequestMSP_SET_COMMAND(self.activeState.commandType)
                self.activeStateAP.commandType = NONE_COMMAND
            elif (self.activeStateAP.commandType != NONE_COMMAND and self.activeState.isAutoPilotOn and (state[7] == 1500)):
                self.MSP.sendRequestMSP_SET_COMMAND(self.activeStateAP.commandType)
                self.activeStateAP.commandType = NONE_COMMAND
            
            sleep(0.022)

    def readThread(self):
        while (self._threadsRunning):
            self.sock.readResponseMSP()
            #self.PID.calculateEstimatedAltitude()

    def serviceThread(self):
        pass

    def reconnect(self):
        self.sock.connect()

    def disconnect(self):
        # TODO : Send command to drone to either (stop moving, stall at one place) or (stop moving, and land) or (just stop everything)
        self.control.kill()
        sleep(0.1)
        if (self._threadsRunning):
            self._threadsRunning = False
            self._threads[0].join()
            self._threads[1].join()
        self.sock.disconnect()

    def start(self):
        self._threadsRunning = True
        self.targets = []
        writeThread = threading.Thread(target=self.writeThread)
        writeThread.start()
        readThread = threading.Thread(target=self.readThread)
        readThread.start()
        self._threads = [writeThread, readThread]
        self.status = 1 # Running

    def start1(self):
        self._threadsRunning = True
        self._threads = []
        for proc in self.target_threads:
            _t_thread = threading.Thread(target=proc)
            _t_thread.start()
            self._threads.append(_t_thread)
        self.status = 1
    
