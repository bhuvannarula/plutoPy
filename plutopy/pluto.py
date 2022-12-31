from time import sleep
from protocol import *
from commands import *
import threading

class plutoDrone():
    def __init__(self, IP_ADDRESS : str, CAMERA_IP_ADDRESS : str = '', PORT : int = 23, CAMERA_PORT :int = 9060) -> None:
        
        # False -> Threads Stop Running
        self._threadsRunning = True
        self._threads =  []

        # Step 0 : Initialize the State Instances of Drone
        self.activeState = plutoState()
        self.activeStateAP = plutoState()
        self.responseState = plutoState()

        # Step 1 : Initialize the Read Buffer for Drone
        self.buffer = plutoBuffer()

        # Step 2 : Initialize the socket for Drone
        self.sock = plutoSock(IP_ADDRESS, PORT, self.buffer, self.responseState)
        
        # Step 3 : Connecting to Socket
        self.sock.connect()

        # Step 4 : Initialize MSP Instance
        self.MSP = plutoMSP(self.sock)

        # Attaching command controls to class
        self.cmd = plutoControl(self.activeState)
    
    def writeThread(self):
        requests = [MSP_RC, MSP_ATTITUDE, MSP_RAW_IMU, MSP_ALTITUDE, MSP_ANALOG]

        self.MSP.sendRequestMSP_ACC_TRIM()

        while (self._threadsRunning):
            state = self.activeState.array()
            if (self.activeState.isAutoPilotOn and state[7]):
                state[0] += self.activeStateAP.rcRoll - 1500
                state[1] += self.activeStateAP.rcPitch - 1500
                state[2] += self.activeStateAP.rcThrottle - 1500
                state[3] += self.activeStateAP.rcYaw - 1500
            
            self.MSP.sendRequestMSP_SET_RAW_RC(state)
            self.MSP.sendMulRequestMSP_GET_DEBUG(requests)

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

    def serviceThread(self):
        pass


    def disconnect(self):
        # TODO : Send command to drone to either (stop moving, stall at one place) or (stop moving, and land) or (just stop everything)
        self._threadsRunning = False
        self.sock.disconnect()

    def start(self):
        self._threadsRunning = True
        writeThread = threading.Thread(target=self.writeThread)
        writeThread.run()
        readThread = threading.Thread(target=self.readThread)
        readThread.run()
        self._threads = [writeThread, readThread]
