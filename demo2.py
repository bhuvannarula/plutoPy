from aruco.plutoCV import *
import threading
from plutopy import plutoDrone

drone = plutoDrone('192.168.4.1')

drone.start()

drone.reconnect()

drone.reconnect()

state = arucoState()

def cvThread():
    aruco = arucoGPS(state)

_thread = threading.Thread(target=cvThread)
_thread.start()

# Drone should be facing right
# Increasing X means moving forward
# If moving forward, decrease pitch_trim by 1

# Inreasing Y means moving right
# If moving right, decrease pitch_roll by 1



def dronepid():
    sleep(3)
    def maxlimit(Y : float, lim : float):
        if Y > lim:
            return (lim)
        elif Y < -lim:
            return (-lim)
        else:
            return Y
    fix_state = arucoState()
    iter_n = 10
    for _i  in range(iter_n):
        fix_state.X += state.X
        fix_state.Y += state.Y
        fix_state.Z += state.Z
    fix_state.X = int(fix_state.X*4/iter_n)/4
    fix_state.Y = int(fix_state.Y*4/iter_n)/4
    fix_state.Z = int(fix_state.Z*4/iter_n)/4

    trim_roll = 0
    trim_pitch = 0

    print(fix_state)
    drone.control.take_off()

    #sleep(2)

    sleep_f = 0.05
    while True:
        sleep(sleep_f)
        _err = [
            state.X - fix_state.X,
            state.Y - fix_state.Y,
            state.Z - fix_state.Z
        ]

        #print(_err)
        trim_pitch = -int(_err[0]*0)
        trim_roll = -int(_err[1]*1)

        '''
        if _err[0] > 0.25:
            trim_pitch -= 3
        elif _err[0] < -0.25:
            trim_pitch += 3
        else:
            trim_pitch = 0

        if _err[1] > 0.25:
            trim_roll -= 3
        elif _err[1] < -0.25:
            trim_roll += 3
        else:
            trim_roll = 0
        '''

        _t_pit = maxlimit(trim_pitch, 50)
        _t_rol = maxlimit(trim_roll, 50)
        print(_t_rol, _t_pit)
        try:
            #drone.MSP.sendRequestMSP_SET_ACC_TRIM(_t_rol, _t_pit)
            drone.activeState.rcRoll = 1500+_t_rol
            drone.activeState.rcPitch =  1500+_t_pit
            drone.activeState.rcThrottle = 1600
        except:
            pass
        trim_pitch = _t_pit
        trim_roll = _t_rol

_thread1 = threading.Thread(target=dronepid)
_thread1.start()
sleep(10)
drone.control.land()

#drone.disconnect()