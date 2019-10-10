#! /bin/bash

# # Make sure Port is accessible by mavros
# sudo chmod 777 /dev/ttyACM0

# Roscore 
roscore &
sleep 5

# Launch mavros script
roslaunch meen_machine px41.launch &
sleep 10;

# Launch RC Override node
rosrun meen_machine mavrosrc.py &
sleep 5;

# Launch either joystick or autonomous control

# Launch the state machine
rosrun meen_machine fsm.py &


trap 'kill $BGPID; killall rosmaster; killall roscore; exit' SIGINT SIGTERM

wait
