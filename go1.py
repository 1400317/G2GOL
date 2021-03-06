
#!/usr/bin/env python

import roslib
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
import math
from math import pi

## Robot 1 Positions
# Current Position
x1 = 0
y1 = 0
theta1 = 0
# Target Position
xg1 = 0
yg1 = 0

## Robot 2 Positions
# Current Position
x2 = 0
y2 = 0
theta2 = 0
# Target Position
xg2 = 0
yg2 = 0

## Robot 3 Positions
# Current Position
x3 = 0
y3 = 0
theta3 = 0
# Target Position
xg3 = 0
yg3 = 0

## Robot 4 Positions
# Current Position
x4 = 0
y4 = 0
theta4 = 0
# Target Position
xg4 = 0
yg4 = 0

def Robot1(pos):
    global x1, y1, theta1
    x1 = pos.data[0]
    y1 = pos.data[1]
    theta1 = pos.data[2]

def Robot2(pos):
    global x2, y2, theta2
    x2 = pos.data[0]
    y2 = pos.data[1]
    theta2 = pos.data[2]

def Robot3(pos):
    global x3, y3,theta3
    x3 = pos.data[0]
    y3 = pos.data[1]
    theta3 = pos.data[2]

def Robot4(pos):
    global x4, y4, theta4
    x4 = pos.data[0]
    y4 = pos.data[1]
    theta4 = pos.data[2]

def goal1(head):
    global xg1, yg1
    xg1 = head.data[0]
    yg1 = head.data[1]

def goal2(head):
    global xg2, yg2
    xg2 = head.data[0]
    yg2 = head.data[1]

def goal3(head):
    global xg3, yg3
    xg3 = head.data[0]
    yg3 = head.data[1]

def goal4(head):
    global xg4, yg4
    xg4 = head.data[0]
    yg4 = head.data[1]

def get_twist(x, y, theta, x_g, y_g):
    # arguments are the robot's pose in the global reference frame
    # get the error in the global reference frame
    error_x  = x_g  - x
    error_y  = y_g  - y

    if((error_x>=-3) and (error_x<=3)):
      error_x = 0
    if((error_y>=-3) and (error_y<=3)):
      error_y = 0

    # get the error in the robot's reference frame
    gr_x  = error_x*math.cos(theta)  + error_y*math.sin(theta)
    gr_y  = -error_x*math.sin(theta) + error_y*math.cos(theta)
    # calculate rho and alfa
    rho  = math.sqrt(gr_x**2+gr_y**2)
    alfa = math.atan2(gr_y,gr_x)
    # define controller gains
    K_RHO = 2.5 # 0.6 doesn't work fine with me
    #(robot becomes unstable a bit after arriving to the desired pose)
    K_ALPHA = 1.6; K_THETA = 0.5
    #calculate control commands
    v     = K_RHO*rho                    # v = linear velocity command
    omega = K_ALPHA*alfa                 # omega = angular velocity command
    # return th control commands
    twist = Twist()
    twist.linear.x  = v; twist.linear.y  = 0; twist.linear.z  = 0;
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = omega;
    return twist

def gtg_talker():
    rospy.init_node('go_to_goal')
    rospy.loginfo("%s started" % rospy.get_name())

    #Subscribers
    rospy.Subscriber('rob1_CurrentPose', Int32MultiArray,Robot1)
    rospy.Subscriber('rob2_CurrentPose', Int32MultiArray,Robot2)
    rospy.Subscriber('rob3_CurrentPose', Int32MultiArray,Robot3)
    rospy.Subscriber('rob4_CurrentPose', Int32MultiArray,Robot4)
    rospy.Subscriber('goal1', Int32MultiArray, goal1)
    rospy.Subscriber('goal2', Int32MultiArray, goal2)
    rospy.Subscriber('goal3', Int32MultiArray, goal3)
    rospy.Subscriber('goal4', Int32MultiArray, goal4)

    #Publishers
    cmd_vel_publisher1 = rospy.Publisher('R1', Twist, queue_size = 10)
    cmd_vel_publisher2 = rospy.Publisher('R2', Twist, queue_size = 10)
    cmd_vel_publisher3 = rospy.Publisher('R3', Twist, queue_size = 10)
    cmd_vel_publisher4 = rospy.Publisher('R4', Twist, queue_size = 10)

    #Publishing Rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #Get Twist Messages
        twist1 = get_twist(x1, y1, theta1, xg1, yg1)
        twist2 = get_twist(x2, y2, theta2, xg2, yg2)
        twist3 = get_twist(x3, y3, theta3, xg3, yg3)
        twist4 = get_twist(x4, y4, theta4, xg4, yg4)

        #Publish Twist Messages
        cmd_vel_publisher1.publish(twist1)
        cmd_vel_publisher2.publish(twist2)
        cmd_vel_publisher3.publish(twist3)
        cmd_vel_publisher4.publish(twist4)

        #Sleep to get required publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        gtg_talker()
    except rospy.ROSInterruptException:
        pass
    finally:
rospy.loginfo("%s closed" % rospy.get_name())
