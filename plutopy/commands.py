from common import plutoState

class plutoControl():
    def __init__(self, state : plutoState) -> None:
        self.cmd = state
        
    def arm(self):
        self.cmd.rcRoll = 1500
        self.cmd.rcYaw = 1500
        self.cmd.rcPitch = 1500
        self.cmd.rcThrottle = 1000
        self.cmd.rcAUX4 = 1500
        self.cmd.isAutoPilotOn = 0

    def box_arm(self):
        self.cmd.rcRoll = 1500
        self.cmd.rcYaw = 1500
        self.cmd.rcPitch = 1500
        self.cmd.rcThrottle = 1500
        self.cmd.rcAUX4 = 1500
        self.cmd.isAutoPilotOn = 0

    def disarm(self):
        self.cmd.rcThrottle = 1300
        self.cmd.rcAUX4 = 1200

    def indentify_key(self, msg):
        self.key_value = msg.data

        if self.key_value == 70:
            if(self.cmd.rcAUX4 == 1500):
                self.disarm()
            else:
                self.arm()
        elif self.key_value == 10:
            self.forward()
        elif self.key_value == 30:
            self.left()
        elif self.key_value == 40:
            self.right()
        elif self.key_value == 80:
            self.reset()
        elif self.key_value == 90:
            if(self.cmd.isAutoPilotOn == 1):
                self.cmd.isAutoPilotOn = 0
            else:
                self.cmd.isAutoPilotOn = 1
        elif self.key_value == 50:
            self.increase_height()
        elif self.key_value == 60:
            self.decrease_height()
        elif self.key_value == 110:
            self.backward()
        elif self.key_value == 130:
            self.take_off()
        elif self.key_value == 140:
            self.land()
        elif self.key_value == 150:
            self.left_yaw()
        elif self.key_value == 160:
            self.right_yaw()
        self.command_pub.publish(self.cmd)

    def forward(self):
        self.cmd.rcPitch = 1600

    def backward(self):
        self.cmd.rcPitch = 1400

    def left(self):
        self.cmd.rcRoll = 1400

    def right(self):
        self.cmd.rcRoll = 1600

    def left_yaw(self):
        self.cmd.rcYaw = 1200

    def right_yaw(self):
        self.cmd.rcYaw = 1800

    def reset(self):
        self.cmd.rcRoll = 1500
        self.cmd.rcThrottle = 1500
        self.cmd.rcPitch = 1500
        self.cmd.rcYaw = 1500
        self.cmd.commandType = 0

    def increase_height(self):
        self.cmd.rcThrottle = 1800

    def decrease_height(self):
        self.cmd.rcThrottle = 1300

    def take_off(self):
        self.disarm()
        self.box_arm()
        self.cmd.commandType = 1

    def land(self):
        self.cmd.commandType = 2