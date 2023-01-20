# plutoPy
A Python Wrapper for Controlling Pluto Drone
(tested on Pluto 1.2)

## Installing the Package
(Requirements : Python >= 3.6)

The Package can be installed by running the following pip command, (requires Git)

    pip install git+https://github.com/bhuvannarula/plutoPy.git#egg=plutopy

## Using the Package
The package, at its heart, creates a drone class that is used for doing any task.
To import it, simply run the following code(s),

#### For a Drone,
    from plutopy import plutoDrone
For further use, refer to 'example_BasicControls.py' script in GitHub Repo

#### For a Swarm
    from plutopy import plutoSwarm
For further use, refer to 'example_DroneSwarm.py' script in GitHub Repo
