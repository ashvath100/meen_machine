#! /usr/bin/python

import rospy
import sys
import time

import numpy as np

from geometry_msgs.msg import *
from mavros_msgs.msg import *

class MavrosRC(object):

    def __init__(self):

        rospy.init_node("mavrosrc_node")
        rospy.loginfo("in mavrossrc init")
        self.rc_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=1)

        self.rc_sub = rospy.Subscriber("/mavros/setpoint_velocity/cmd_vel", TwistStamped, self.rc_callback)

    def rc_callback(self, vel):

        # kPeriod = 0.1
# Channel	Meaning
# 1	Pitch
# 2	Roll
# 3	Throttle
# 4	Yaw
# 5	Forward
# 6	Lateral
# 7	Camera Pan
# 8	Camera Tilt
# 9	Lights 1 Level
# 10 Lights 2 Level
# 11 Video Switch

        msg = OverrideRCIn()

        msg.channels[0] = 1500
        msg.channels[1] = 1500
        msg.channels[2] = self.speedToPpm(vel.twist.linear.z)
        msg.channels[3] = 1500
        msg.channels[4] = self.speedToPpm(vel.twist.linear.x)
        msg.channels[5] = 1500
        msg.channels[6] = 1500

        self.rc_pub.publish(msg)

    def angleToPpm(self, angle):
        neg_M_PI = 1000
        M_PI = 2000
        ppm = (angle - (neg_M_PI)) / (M_PI - (neg_M_PI)) * (1000) + 1000

        return ppm

    def speedToPpm(self, speed):
        return 1500 + speed * 400.0

def main():
    mavrc = MavrosRC()
    rospy.spin()

if __name__ == "__main__":
    main()
