from plutopy import plutoSwarm
from swarmArUco import swarmArUco, makeSure

swarm = plutoSwarm()

# Master Drone
swarm.add(0, "192.168.4.1", 23)

# Slave Drone
swarm.add(1, "192.168.4.1", 23)

# Start Communication with Drones
swarm.start()

# Set drones to throttle mode, as we will be using manual PID through ArUco Detection
swarm[0].control.throttleMode()
swarm[1].control.throttleMode()

# Creating a dictionary with {droneName : ArUcoID}
IDdict = {
    0 : 5,
    1 : 85
}

# Creating a Swarm Instance for plutoSwarm
aruco = swarmArUco(swarm, IDdict)

# Setting Origin for all drones in swarm
aruco.setOrigins()

# Setting initial targets as starting coordinates, at set Z height (in cm)
# Not doing so may lead to crashed among drones.
aruco.originTarget()

# Once initial targets are set, we can take-off drones.
aruco.take_off_all()

# Starting the PID Controllers for all drones in swarm
aruco.start()

altitude = 90
position0 = [-50, -25, altitude]
position1 = [50, -25, altitude]

class plutoFollower:
    def __init__(self, position0 : list, position1 : list) -> None:
        self.last_position = position0
        self.current_position = position1

    def starting(self):
        # Drone 1 (Master Drone) to position1
        aruco[0].setTarget(*self.current_position)
        makeSure(aruco[0])

        # Drone 2 (Slave Drone) to position0
        aruco[1].setTarget(*self.last_position)
        makeSure(aruco[1])
    
    def nextpoint(self, target : list):
        self.last_position = self.current_position
        self.current_position = target

        # Drone 1 (Master) moves to new point
        aruco[0].setTarget(*self.current_position)
        makeSure(aruco[0])

        # Drone 2 (Slave) moves to previous point of Master
        aruco[1].setTarget(*self.last_position)
        makeSure(aruco[1])

follower = plutoFollower(position0, position1)
follower.starting()

position2 = [50, 25, altitude]
follower.nextpoint(position2)

position3 = [-50, 25, altitude]
follower.nextpoint(position3)

position4 = position0
follower.nextpoint(position4)

position5 = position1
follower.nextpoint(position5)

# Now, wait until user presses 'Enter' key, then stop all code, and close the sockets.
_ = input()
aruco.stop()
