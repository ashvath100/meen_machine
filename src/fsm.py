#! /usr/bin/python

from motion_planner import *
import rospy
import sys
import time

import numpy as np
class FSM(object):
    def __init__(self, sim):
        self.sim = sim
        self.controller = Controller(self.sim)

    def fsm_start(self):
        
        while (True and not self.sim):
            data = self.controller.changeToDepthHold()
            if data == False:
                 rospy.loginfo("Depth Mode Failed, Retrying")
            else:
                break

        while (True and not self.sim):
            data = self.controller.doArming()
            if data == False:
                rospy.loginfo("Arming Failed, Retrying")
            else:
                break
        
        self.Throttle(-0.19, 7)
        self.Forward(0.4, 15)

    def Throttle(self, speed, sec):
    # Add distance or seconds

        vel = TwistStamped()
        vel.twist.linear.z = speed

        rospy.loginfo("Starting Dive at Speed: " + str(vel.twist.linear.z))
        start_time = time.time()

        # sleep rate
        while time.time() <= start_time + sec:
            self.controller.pub_cmd_vel.publish(vel)
            rospy.sleep(0.5)

        vel = TwistStamped()
        vel.twist.angular.z = 0.0
        self.controller.pub_cmd_vel.publish(vel)
        rospy.sleep(1)
        rospy.loginfo("Dive")  


    def Forward(self, speed, sec):
    # Add distance or seconds

        vel = TwistStamped()
        vel.twist.linear.x = speed
        rospy.loginfo("Starting Forward at Speed: " + str(vel.twist.linear.x))
        start_time = time.time()

        # sleep rate
        while time.time() <= start_time + sec:
            self.controller.pub_cmd_vel.publish(vel)
            rospy.sleep(0.5)

        vel = TwistStamped()
        vel.twist.angular.x = 0.0
        self.controller.pub_cmd_vel.publish(vel)
        rospy.sleep(1)
        rospy.loginfo("Forward")  

def main():

    rospy.init_node("fsm")

    if len(sys.argv) > 1:
        if sys.argv[1] == "--sim":
            fsm = FSM(True)
    else:
        fsm = FSM(False)

    fsm.fsm_start()

if __name__ == "__main__":
    main()
