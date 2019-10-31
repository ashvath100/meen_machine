#!/usr/bin/env python

import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs import Bool


# Pin Definitions:
but_pin = 18

# Flag for Button_state
flag = 0

def talker(self,msg):
    pub = rospy.Publisher('kill_switch', Bool, queue_size=10)
    rospy.init_node('kill_switch', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        self.msg=flag
        pub.publish(self.msg)
        rate.sleep()

# Disarm Pixhawk when button pressed
def Kill(channel):
    flag=1  # Button pressed
    try:
        talker(flag)
    except rospy.ROSInterruptException:
        pass 


def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
    
    GPIO.add_event_detect(but_pin, GPIO.FALLING, callback=Kill, bouncetime=10)
    # print("Starting demo now! Press CTRL+C to exit")
    
    try:
        while True:
            # run talker    
            try:
                talker(flag)
            except rospy.ROSInterruptException:
                pass
    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()