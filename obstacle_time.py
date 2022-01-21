#! /usr/bin/env python

import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def shut_down(pub, rate, msg):

    msg.linear.x = 0
    msg.angular.z = 0
    pub.publish(msg)
    rate.sleep()

def run_command(linear_x, angular_z, t, rate):

    init_time = time.time()

    while(time.time()- init_time < t ):

        range = rospy.wait_for_message('/scan', LaserScan).ranges[0]  # We subscribe to the laser's topic

        print(range)

        if range >= 0.4:
            msg.linear.x = linear_x
            msg.angular.z = angular_z

        else:
            msg.linear.x = 0
            msg.angular.z = 0

        pub.publish(msg)
        rate.sleep()

    shut_down(pub, rate, msg)

def run(pub, rate, msg):

    run_command(0.1, 0, 30, rate)

if __name__== '__main__':

    rospy.init_node('waypoint')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    msg = Twist()
    rate = rospy.Rate(10)

    try:
        run(pub, rate, msg)
    except rospy.ROSInterruptException:
        shut_down(pub, rate, msg)
        pass
