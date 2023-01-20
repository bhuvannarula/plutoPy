from plutopy import plutoSwarm

# Initializing a Swarm Instance
swarm = plutoSwarm()

# Adding drones to swarm
swarm.add(0, '192.168.4.1', 23)
swarm.add('pluto', '192.168.4.1', 23)

# Listing IDs of Drones in Swarm
ids = swarm.list_names()
print(ids)

# Connecting to Drones in Swarm
swarm.start('pluto') # -> Only connects 'pluto' ID Drone
swarm.start() # -> Connects all Drones in Swarm
print(swarm.status('pluto')) # -> Returns status of 'pluto' Drone

# Basic Drone Controls
# swarm[ID] -> Returns a plutoDrone instance, same as individual drone.
swarm['pluto'].control.take_off()
swarm['pluto'].control.forward()
swarm['pluto'].control.land()

# Disconnect Drone
swarm.stop('pluto') # -> Stops/Disconnects only 'pluto' drone
swarm.stop() # -> Stops/Disconnects all drones in swarm.
print(swarm.status('pluto'))

# Remove a Drone from Swarm
swarm.remove('pluto')