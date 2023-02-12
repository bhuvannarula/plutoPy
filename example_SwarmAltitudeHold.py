from plutopy import plutoSwarm
from swarmArUco import swarmArUco

# Creating a plutoSwarm instance, which allows basic controls of drones, 
# through MSP Communication
swarm = plutoSwarm()

# Master Drone
swarm.add(0, "192.168.87.184", 23)

# Slave Drone
swarm.add(1, "192.168.87.252", 23)

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

target0 = [
    aruco[0].origin.X,
    aruco[0].origin.Y,
    90
]

target1 = [
    aruco[1].origin.X,
    aruco[1].origin.Y,
    90
]

aruco[0].setTarget(*target0)
aruco[1].setTarget(*target1)

# Once initial targets are set, we can take-off drones.
aruco.take_off_all()

# Starting the PID Controllers for all drones in swarm
aruco.start()

# PRESS 'Q' or 'q' to stop camera feed, and disconnect the drone.
_ = input()
aruco.land_all()
aruco.stop()