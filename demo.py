from plutopy import plutoDrone

drone = plutoDrone('192.168.4.1', PORT=23)

drone.control.take_off()

drone.control.forward()
drone.control.left()

drone.control.land()

drone.activeState.accX
drone.activeState.accY
drone.activeState.accZ