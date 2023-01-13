PIDROLL = 0
PIDPITCH = 1
PIDYAW = 2
PIDALT = 3
PIDPOS = 4
PIDPOSR = 5
PIDNAVR = 6
PIDLEVEL = 7
PIDMAG = 8
PIDVEL = 9
PIDUSER = 10

PID_ITEM_COUNT = 11

class profilePID:
    def __init__(self) -> None:
        self.P_f = [4, 4, 15] #[0]*3
        self.I_f = [0.1, 0.1, 0.7] #[0]*3
        self.D_f = [0.03, 0.03, 0.05] #[0]*3

        self.A_level = 4
        self.H_level = 1
        self.H_senstivity = 100

        #self.P8 = [0]*PID_ITEM_COUNT
        #self.I8 = [0]*PID_ITEM_COUNT
        #self.D8 = [0]*PID_ITEM_COUNT
        #                   ALT POS POSR NAVR   MAG  VEL USER
        self.P8 = [0, 0, 0, 100, 100, 30, 25, 0, 40, 120, 0]
        self.I8 = [0, 0, 0,   0,   0,  2, 33, 0,  0,  45, 0]
        self.D8 = [0, 0, 0,  30,   0,  5, 83, 0,  0,   1, 0]

    def reset(self):
        self.P_f = [4, 4, 15] #[0]*3
        self.I_f = [0.1, 0.1, 0.7] #[0]*3
        self.D_f = [0.03, 0.03, 0.05] #[0]*3

        self.A_level = 4
        self.H_level = 1
        self.H_senstivity = 100

        #self.P8 = [0]*PID_ITEM_COUNT
        #self.I8 = [0]*PID_ITEM_COUNT
        #self.D8 = [0]*PID_ITEM_COUNT
        #                   ALT POS POSR NAVR   MAG  VEL USER
        self.P8 = [0, 0, 0, 100, 100, 30, 25, 0, 40, 120, 0]
        self.I8 = [0, 0, 0,   0,   0,  2, 33, 0,  0,  45, 0]
        self.D8 = [0, 0, 0,  30,   0,  5, 83, 0,  0,   1, 0]

    def profile1(self):
        self.P_f = [3.5, 3.5, 15]
        self.I_f = [0.05, 0.05, 0.7]
        self.D_f = [0.02, 0.02, 0.05]

