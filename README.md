# Lane graph navigating TurtleBot

## Overview
This project uses ROS to demonstrate a lane graph navigating Turtlebot. This project is a proof of concept of a tool-delivery robotic solution for the "Factory of the future". The robot performs lane tracking and obstacle avoidance and takes turns on a physical graph depending on its start position and destination.

## Procedure


## Dependencies

* ROS Kinetic
* Catkin
* roscpp package
* std_msgs package
* message_generation package
* OpenCV

## To build
To build the project run the following steps in a terminal:
* Creating a catkin workspace:
```
mkdir catkin_ws
cd catkin_ws
mkdir src
catkin_make
```
* Cloning the repository and building:
```
cd ~/catkin_ws/src
git clone https://github.com/tristandu/GDP-real/tree/final.git
cd ..
catkin_make
```

## To run
```
cd ~/catkin_ws
source devel/setup.bash
roslaunch line_follower_turtlebot bringup.launch
(in another terminal)
roslaunch line_follower_turtlebot lf.launch start:=1 destination:=15
```

## About the creator
Tristan Durey and Jiaqi Lou, graduate students in MSc in Robotics at University of Cranfield, United Kingdom. 
