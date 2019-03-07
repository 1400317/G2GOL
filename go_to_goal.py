#!/usr/bin/env python  

#
# Instructor provided script for Part 2 of Assignment 2 in COMP 4766/6778.
# You should only need to modify this script by commenting or uncommenting
# the lines labelled "STUDENT".
#
# Andrew Vardy
#

import roslib
roslib.load_manifest('comp4766_a2')
import rospy
import math
import tf
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import pi

# STUDENT: Each of the following lines should be uncommented for Tasks 1, 2,
# and 3, respectively.
from smooth1 import SmoothController1
from smooth2 import SmoothController2
from smooth1_tf import SmoothController1TF

if __name__ == '__main__':
    rospy.init_node('go_to_goal')

    # Create a transform listener.
    listener = tf.TransformListener()

    # Create a publisher so that we can output command velocities.
    cmd_vel_publisher = rospy.Publisher('/cmd_vel', Twist)

    # Create the controller object and specify the goal position (in global
    # coordinates).  STUDENT: For Task 1 uncomment only the first line.
    # Similarly for Tasks 2 and 3 uncomment only the second and third line.
    controller = SmoothController1(2, -2)   # controller is the object handller for smoothController1 class
    #controller = SmoothController2(2, -2, pi)
    #controller = SmoothController1TF(listener, 2, -2)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            # Determine the transform from the /odom frame to the 
            # /base_footprint frame.  /odom represents the robot's oodometric
            # frame of reference.  Since the odometry is perfect in the autolab
            # Stage world, /odom remains coincident with the global reference
            # frame.  /base_footprint represents the pose of the robot's base.
            (trans,rot) = listener.lookupTransform('/odom', '/base_footprint', \
                                                   rospy.Time(0))
        except (tf.LookupException, \
                tf.ConnectivityException, tf.ExtrapolationException):
            # The /odom frame doesn't come into existence right away, which
            # will lead to an exception being generated from lookupTransform.
            continue

        # Get the 2-D position and orientation of the robot with respect to the
        # global frame.
        x = trans[0]
        y = trans[1]
        euler_angles = euler_from_quaternion(rot)
        theta = euler_angles[2]

        # Get a twist object from the controller.  STUDENT: For Tasks 1 and 2
        # you should uncomment the first line.  For Task 3 uncomment the second.
        twist = controller.get_twist(x, y, theta)
        #twist = controller.get_twist()

        # Publish the twist message produced by the controller.
        cmd_vel_publisher.publish(twist)

        rate.sleep()
