from plutopy import plutoDrone

drone = plutoDrone('192.168.4.1', PORT=23)

drone.start()
drone.activeState.rcAUX3 = 1800

drone.control.take_off()



'''
drone.control.take_off()
drone.control.forward()
drone.control.left()
drone.control.land()

drone.info.acc() # 3-axis Accelerometer Data, int from [0,65536)
drone.info.gyro() # 3-axis Gyroscope Data, int from [0,65536)
drone.info.mag() # 3-axis Magnetometer Data, int from [0,65536)
drone.info.all9()

drone.control.reset() -> Stalls drone at one place
drone.control.kill() -> Resets, and kills the motors

drone.disconnect() -> Resets, Kills the Motors, and closes the socket.
'''