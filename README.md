# plutoPy

Pure-Python Wrapper for Pluto Drone

# Introduction

**plutoPy** is a pure python wrapper, which enables Python-based remote commands to be used to control the PLUTO drone. This includes connecting to drone through sockets, sending and receiving MSP data, all in python, just by writing simple high-level code

# Contents

- [Getting Started](#getting-started)
    - Pre-Requisites
    - Installation
    - How to Run
- [Usage Instructions](#usage-instructions)
    - Connection
    - Basic Commands
    - Control
    - State & Other Information
    - Key binds
- [Structure and Methodology](#structure-and-methodology)
    - Contents and Hierarchy
    - Working
- [Acknowledgements](#acknowledgements)

# Getting Started

plutoPy is a lightweight package, with its requirements already satisfied in the base installation of Python.

## Prerequisites

Python 3 (tested on ≥ 3.6)

## Installation

Clone the GitHub repository given below, (plutopy is a package, can be copied as required)
[https://github.com/bhuvannarula/plutoPy](https://github.com/bhuvannarula/plutoPy)

For global installation of package,

The package can be installed by running the following pip command, (requires Git)

```powershell
pip install git+https://github.com/bhuvannarula/plutoPy.git
```

## How to Use?

The package, at its heart, creates a drone class that is used for doing any task.
To import it, simply run the following code(s),

### For a Drone,

`from plutopy import plutoDrone`

For further use, refer to [example_BasicControls.py](https://github.com/bhuvannarula/plutoPy/blob/main/example_BasicControls.py) script.

### For a Swarm

`from plutopy import plutoSwarm,`

For further use, refer to [example_DroneSwarm.py](https://github.com/bhuvannarula/plutoPy/blob/main/example_DroneSwarm.py) script.

# Usage Instructions

## Connection

After you have imported *plutoDrone*, use the following commands to establish a connection and open the command line:

`drone = plutoDrone(IP_ADDRESS, PORT)`

All parameters are optional, and a single drone can be easily initialized on default values (IP : 192.168.4.1, PORT : 23)

`drone = plutoDrone()`

To start the connection to drone, and the threads for communicating with drone, just call the function,

`drone.start()`

If the connection fails you can use the following command to reconnect to the drone:

`drone.reconnect()`

If you wish to disconnect you can use:

`drone.disconnect()`

## Basic Commands

**Arming**

To pass any command to the motors, you need to arm the drone first. You can arm using:

`drone.control.arm()`

This will also set the throttle to 1000 by default.

**Box Arm**

Box Arm will set the throttle value to 1500 by default.

`drone.control.boxarm()`

**Disarming**

To disarm the drone:

`done.control.disarm()`

**Take Off**

Disarms the drone, and the drone takes off:

`drone.control.take_off()`

**Land**

Landing reduces the throttle speed at a constant rate before stopping them.

`drone.control.land()`

**Reset**

To reset the drone to its default configuration:

`drone.control.reset()`

**Kill**

To kill the motors:

`drone.control.kill()`

## Control

Following commands can be used to control the drone’s position. To change command values or to reconfigure them, you can find them in ***plutopy/commands.py*** file.

**Forward**

To move the drone forward:

`drone.control.forward()`

By default it will change the pitch value to 1600.

**Backward**

To move the drone backward:

`drone.control.backward()`

By default it will change the pitch value to 1400.

**Left**

To move the drone leftward:

`drone.control.left()`

By default it will change the roll value to 1400.

**Right**

To move the drone rightward:

`drone.control.right()`

By default it will change the roll value to 1600.

**Increase Height**

To increase height at constant acceleration:

`drone.control.increase_height()`

By default it will increase the throttle to 1800.

**Decrease Height**

To decrease height at constant acceleration:

`drone.control.decrease_height()`

By default it will decrease the throttle to 1300.

**Throttle**

To set the throttle to particular value:

`drone.rc.rcThrottle = {value`}

**Pitch & Roll**

To set the trim for pitch and roll:

`drone.control.trimRollPitch({trim_roll_value}, {trim_pitch_value})`

To set roll and pitch to a particular value:

`drone.activeState.rcPitch = {value}
drone.activeState.rcRoll = {value}` 

**Yaw**

To set the drone towards left or right:

`drone.control.right_yaw()
drone.control.left_yaw()`

By default it sets yaw to 1800 & 1200 respectively.

To set the yaw to particular value:

`drone.rc.rcYaw = {value}`

## State & Other Information

**********State**********

To get the state of the drone:

`drone.state.array()`

Returns an array as [Roll,Pitch,Throttle,Yaw,AUX1,AUX2,AUX3,AUX4].
You can find more information regarding the AUX parameters [here](https://docs.google.com/document/d/1c2tjbeAuTYk3JZrkazImayqjCKx9w3rND4RTN41ol6U/edit).

You can get other information by using `drone.state.{X}()`

- {X} can be:
    1. roll
    2. pitch
    3. yaw
    4. battery
    5. rssi
    6. accX
    7. accY
    8. accZ
    9. gyroX
    10. gyroY
    11. gyroZ
    12. magX
    13. magY
    14. magZ
    15. alt
    16. FC_versionMajor
    17. FC_versionMinor
    18. FC_versionPatchLevel
    19. rcRoll
    20. rcPitch
    21. rcYaw 
    22. rcAUX1
    23. rcAUX2
    24. rcAUX3
    25. rcAUX4
    26. trim_roll
    27. trim_pitch
    28. commandType
    29. isAutoPilotOn

************************************Sensor Information************************************

All in order [x,y,z].

From Gyroscope:

`drone.info.gyro()`

From Accelerometer:

`drone.info.acc()`

From Magnetometer:

`drone.info.mag()`

From all the three sensors:

`drone.info.all9()`

# Structure And Methodology

## Contents and Hierarchy

Following are the contents of the wrapper:

1. **__init__.py**
    
    Declaration for module.
    
2. **common.py**
    
    Some commonly used functions.
    
3. **plutostate.py**
    
    Contains plutoState class, which stores state data of drone.
    
4. **plutoinfo.py**
    
    Sensor information.
    
5. **reader.py**
    
    Serial Reader for response from the Drone.
    
6. **plutosock.py**
    
    Class for connecting to drone through sockets.
    
7. **protocol.py**
    
    Class for creating and receiving MSP Packets for communication.
    
8. **commands.py**
    
    Class for Control commands.
    
9. **pluto.py**
    
    Main plutoDrone class, which stitches all the classes together.
    
10. **plutoswarm.py**
    
    Class for easy initialization of Pluto Drone Swarm.
    

## Working

This wrapper works through a multi-threaded method, in which different threads are responsible for sending and receiving the data from drone. The connection with the drone is implemented using the MSP protocol. Different aspects of the wrapper are explained below.

### Socket

The communication with drone is through low-level sockets, in which requests are sent from client (computer) to host (drone), and response is received.

### Threading

Mainly two threads are initialized for communication, one for sending requests with data to drone, and another thread for receiving response from drone. In this manner, independent two-way communication with drone is implemented.

### Protocol

A modified version of the Multiwii Serial Protocol (MSP) is used by Pluto. There are many packets designed specifically for flight based controllers in this protocol. These packets are manually created in the package, and sent to drone over sockets. More information on this protocol is available at [Multiwii](http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol#mw-head), or in this [document](https://docs.google.com/document/d/1c2tjbeAuTYk3JZrkazImayqjCKx9w3rND4RTN41ol6U/edit).

### Integration

All components are integrated using the ********[pluto.py](https://github.com/bhuvannarula/plutoPy/blob/main/plutopy/pluto.py)******** file through **************plutoDrone************** class which initialises the socket, necessary threads and states,  and the control interface, which enable the package to control the drone.

# Acknowledgements

The base logic of this wrapper has been derived from the C++ logic implemented in the Pluto ROS Package, and has been highly customized to make it reliable and easy to use.

[GitHub - DronaAviation/pluto-ros-package: This package canbe used to control Pluto using keyboard, joystick or rostopic](https://github.com/DronaAviation/pluto-ros-package)