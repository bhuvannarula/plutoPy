from plutopy import plutoDrone

# Creating a plutoDrone instance
drone = plutoDrone()

# Starting the MSP communication with drone
drone.start()

# Incase connection fails, reconnect to drone
drone.reconnect()

# Now, we are communicating through MSP, and can perform basic commands
drone.control.take_off()

drone.control.forward()
drone.control.backward()
drone.control.left()
drone.control.right()
drone.control.increase_height()
drone.control.decrease_height()
drone.control.left_yaw()
drone.control.right_yaw()

drone.control.land()

# To access the IMU data,
print(drone.info.acc()) # -> Returns 3-axis Accelerometer Data
print(drone.info.gyro()) # -> Returns 3-axis Gyroscope Data
print(drone.info.mag()) # -> Returns 3-axis Magnetometer Data
print(drone.info.all9()) # Returns DICTIONARY with all 9 axis data

# For accessing specific values,
drone.state.accX
drone.state.gyroX
drone.state.magX
drone.state.battery
drone.state.rssi

# For setting specific values,
drone.activeState.rcAUX1 = 1000
drone.activeState.rcRoll = 1500
drone.activeState.rcPitch = 1500
drone.activeState.rcYaw = 1500
drone.activeState.rcThrottle = 1500

# To reset the state of drone (roll)
drone.control.reset()

# To disconnect from drone, and close communications
drone.disconnect()