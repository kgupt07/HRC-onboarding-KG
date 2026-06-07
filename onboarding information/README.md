# HRC Software Onboarding Fall 2025
![Demo](../dog.gif)

This document walks you through the onboarding task for HRC Software such that by the end of this onboarding project, you will have created a (semi) walking quadruped simulated on your computer.\
\
For this onboarding project, you will make a mujoco xml specification of a robot dog, simulate it in a python simulation loop, and write a PD controller and walking program for it in simulation.\
\
The goal of this onboarding is for you to get some familiarity with the world of programming legged robots such as thinking about robots and their control physically (kinematics) and the usage of simulation. During this project, you cannot solely rely on the readme and are encouraged to read a bit more about legged locomotion and robotics.

## Experience Assumptions
This project assumes basic familiarity with Python programming, programming with vectors (numpy), git and common software management practices. All the following steps about installation and setting up environments are done on linux terminal. Don’t worry if you are not familiar with these skills, they can be picked up quickly and are always useful.

## System Requirements
Linux based computer, emulator (mac OS), wsl

# Robotics Simulation
Simulation is very important in robotics and other complicated systems because legged robots are to expensive and fragile to do trial and error techniques on real hardware. Thus we would like to test our control software in simulation before deploying it on real hardware. \
\
In simulation, we model legged robots as rigid bodies connected by rotary joints with each joint representing (with caveats) a real life motor. The simulation is used to test control software which controls the robot by outputting joint torques (the lowest level abstraction to hardware) to the motors.
# Python Environment
Good python programming practice necessitates the use of virtual environments to have a python interpreter that has the packages you need. 

(If you are familiar with python environments, install environments however you like with numpy as mujoco)

In your projects folder, make a python venv with:

```
python3 -m venv [your env name here]
```

This will make a folder of your env name that contains the python interpreter of the virtual environment. You will know it is active in your terminal by the presence of the ([env name]) before your user name and directory. You can activate and deactivate the venv with:
```
source [your env name]/bin/activate // run the bash file to activate the venv
deactivate // deactivate the venv
```
With your venv activated, install mujoco and numpy with
```
pip install mujoco
pip install numpy
```
# Mujoco Snake Example
![Demo2](snake.gif)
To help you get started, this github repo contains an example python script simulating a snake in mujoco. Clone this repository into your local machine with:
```
git clone https://github.com/humanoid-purdue/onboarding-fall25
```
And with your set up environment with mujoco you can run:
```
python visualize_snake.py
```
To see a gui with a snake flopping around on the floor.
## File Structure 
This repo contains two files, snake.xml and visualize_snake.py. snake.xml contains the specification of the snake robot in the simulation. The details of how the specification works can be found online. visualize_snake.py generates a model and data variable from the xml, and runs a single timestep through mj_step(model, data) before visualizing with viewer2. model represents the physical properties of the world and data represents the state of the world at a certain timestep. At each timestep, joint torques in the form of a numpy array is loaded into data.ctrl.\
\
The state of the simulation (including all the joint positions) is printed out to the screen as a 11 dimension vector in data.qpos. The first 3 elements represent the xyz position of the robot, the next 4 are a quaternion representing the orientation of the robot and the last 4 elements represents the joint position of each joint. The velocity information is stored in data.qvel.

# Onboarding Task
Create a public repo on your personal github to submit all your work. You will be submitting a github link to your public repo containing all the code for your dog.
## Robot Dog Dimensions
![dog](dog_dims.jpg)
\
Create a mujoco xml that creates a robot similar to the one displayed here. Implement each joint with <motor> actuator with a maximum torque of 20 Nm. **Do not use mujoco's prebuilt position actuators**.
## Robot Dog Simulation Loop
Write a simulation loop similar to visualize_snake.py that loads the robot dog into a simulation gui.
## Robot Dog Controller
Controlling joint torques is unintuitive for the programmer. One way to move from the complicated task of controlling through torque to something like controlling through position is through a joint controller. Implement a PD controller in your control loop using qpos and qvel. Control torque is determined by:\
$$\tau = K_p (X_{des} - X) + K_d (\dot{X}_{des} - \dot{X})$$\
$$\tau:$$ Joint Torques;\
$$K_p \approx 10, K_d \approx 1.0$$: PD gains (feel free to adjust);\
$$X$$: Joint positions (real and desired); $$\dot{X}$$: Joint velocities (real and desired)
## Robot Dog Walking
Finally using your working PD controller, think about the steps needed to do the motions for walking and implement them in your control loop as a function of time. It does not need to be perfect (and most certainly wont because of the open loop nature) and just needs to demonstrate forward locomotion. The requirements for forward locomotion is a mean forward velocity >0.20 m/s and a mean lateral velocity no greater than 0.10 m/s at all times. The base velocity in world frame can be derived from ```data.qvel```
# Submission
DM the software lead **Ludwig Tay** on discord once you are done for review of submission.

# Extra Credit
One area of interest in robotics is Reinforcement Learning control. Reinforcement Learning is used to learn a policy network that takes observations (a vector) from sensor input and outputs action, a joint position target for the PD controller. While RL is very important in robotics, learning about it is not so straightforward, especially many topics in RL is still poorly understood. For this extra credit task, through self study and ingenuity:
1) Run the [mujoco playground](https://github.com/google-deepmind/mujoco_playground/tree) locomotion training script in google colab (free tier should be sufficient for the Go1 Task), try to read into the code to understand how it works.
2) Using the mujoco xml dog created earlier, create your own repo and using mujoco playground, train a walking policy for the robot dog. Study how ```mujoco_playground/_src/locomotion/go1``` registers an environment for training.
3) Submit the repo along with colab environment to train, run and demonstrate the walking policy on your own robot dog.
