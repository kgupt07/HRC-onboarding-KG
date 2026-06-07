# Reading Packet for Understanding Humanoid Robot Control
This document provides resources for understanding humanoid robot control. We expect software members to read enough to understand at a high level how humanoid robot controllers work. We do not expect every software member to read enough to contribute in implementation though those who seek to be more involved should read more in depth to understand implementation.
# Conceptual
## Locomotion
For NEMO, we train a policy network through reinforcement learning to walk. At a high level, this means we create a function that takes a simulation state at a certain time and assigns a reward based on how well we are walking. Through hundreds of millions of trials, we can create a gradient map of action versus reward through PPO and thus train a policy network to maximize reward and walking. \
\
We provide reading on reinforcement learning, reward shaping, as well as model based control to give a better conceptual understanding of how to control a Bipedal Robot.
### Reinforcement Learning
PPO, main reinforcement learning algorithim used today: [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)\
\
Reward function for walking: [DeepWalk: Omnidirectional Bipedal Gait by Deep Reinforcement Learning](https://arxiv.org/pdf/2106.00534)\
\
Phase reward for walking; **important paper**: [Sim-to-Real Learning of All Common Bipedal Gaits via Periodic Reward Composition](https://arxiv.org/abs/2011.01387)\
\
Polynomial foot height tracking: [Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning](https://arxiv.org/html/2408.14472v1)
### Model Based Control
Series of blog posts talking about how older controllers for humanoid robots work. Provides physics intuition as to how humanoid robots move **important**: [https://scaron.info/robotics/how-do-biped-robots-walk.html]\
\
SOTA model based walking controller: [Stair Climbing using the Angular Momentum Linear Inverted Pendulum Model and Model Predictive Control](https://arxiv.org/abs/2307.02448)
# Application
## Reinforcement Learning
While you may be familiar with Mujoco from the onboarding project, we use a GPU accelerated version of Mujoco known as MJX to do efficient training: [https://mujoco.readthedocs.io/en/stable/mjx.html]\
\
We use the brax framework for PPO algorithims: [https://github.com/google/brax/tree/main/brax]\
\
Our reward functions and RL environment is based off Mujoco Playground: [https://github.com/google-deepmind/mujoco_playground]
## ROS2
The code that actually runs on the robot runs on ROS2 along with its simulator Gazebo. ROS2 is tricky to learn and many people have difficulty getting it to run on their computers (It is intended to run on linux systems only). Get started by going through the examples on your machine: [https://docs.ros.org/en/kilted/index.html]
