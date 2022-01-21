#! /usr/bin/env python

import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def shut_down(pub1, pub2, rate, msg):
    print('Shutting down')
    msg.linear.x = 0
    msg.angular.z = 0
    pub1.publish(msg)
    pub2.publish(msg)
    rate.sleep()

def run_command(linear_x, angular_z, t, rate):

    init_time = time.time()

    while(time.time()- init_time < t ):

        range_1 = rospy.wait_for_message('/robot1/scan', LaserScan).ranges[0]  # subscribe to the laser's topic
        range_2 = rospy.wait_for_message('/robot2/scan', LaserScan).ranges[0]  # subscribe to the laser's topic

        print("Robot 1 = ")
        print(range_1)
        print("Robot 2 = ")
        print(range_2)

        if range_1 >= 0.4 or range_2 >= 0.4:
            msg.linear.x = linear_x
            msg.angular.z = angular_z

        else:
            print('Object detected)')
            msg.linear.x = 0
            msg.angular.z = 0

        pub1.publish(msg)
        pub2.publish(msg)
        rate.sleep()

    shut_down(pub1, pub2, rate, msg)

def run(pub1, pub2, rate, msg):

    run_command(0.1, 0, 30, rate)

if __name__== '__main__':

    rospy.init_node('waypoint')
    pub1 = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=10)
    msg = Twist()
    rate = rospy.Rate(10)

    try:
        run(pub1, pub2, rate, msg)
    except rospy.ROSInterruptException:
        shut_down(pub1, pub2, rate, msg)
        pass
