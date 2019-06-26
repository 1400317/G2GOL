#!/usr/bin/env python
"""
"""
import roslib
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Byte
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
import math
from math import pi

i = 0
    #Publishers
cmd_vel_publisher1 = rospy.Publisher('cmd_vel_rob4', Twist, queue_size = 5)
cmd_vel_publisher2 = rospy.Publisher('gtg_flag_rob4',Byte , queue_size = 5)

## Robot 4 Positions
# Current Position
x = 0
y = 0
theta = 0
# Target Position
xyg = list()

def Robot4(pos):
    global x, y, theta
    x = pos.data[0]
    y = pos.data[1]
    theta = pos.data[2]/100.0 #in rad

def goal4(head):
    global xyg
    xyg = head.data
    #get_twist(x,y,theta,xyg)
    #print("goal4")

def gtg_talker():
    rospy.init_node('go_to_goal')
    rospy.loginfo("%s started" % rospy.get_name())
    #print("talker")
    #Subscribers
    rospy.Subscriber('rob4_CurrentPose', Int32MultiArray,Robot4)
    rospy.Subscriber('Planning_Output4', Int32MultiArray, goal4)
    #Publishing Rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        get_twist(x, y, theta, xyg)
        #Sleep to get required publishing rate
        rate.sleep()

def get_twist(x, y, theta, xy_g):# arguments are the robot's pose in the global reference frame
    global i
    #print("i",i)
    #print(len(xy_g))
    if i==0:
        i = len(xy_g)
        print("i",i)
	#print (len(xy_g))
	#print (xy_g)
    if i>0:
        flage=0
        if (i%2 == 0):
            i-=1
        print("i",i)
        #x_g = xy_g[i-1]
#for map 1
        x_g = ((xy_g[i])-1)*17.5
#for map 2
        #x_g = ((xy_g[i])-1)*25
        print(x)
        print('x',x_g)
        #y_g = xy_g[i]
#for map 1
        y_g = ((xy_g[i-1])-1)*17.5
#for map 2
        #y_g = ((xy_g[i-1])-1)*25
        print(y)
        print('y',y_g)
        #print("in while1")
        if(flage==0):
            # get the error in the global reference frame
            error_x  = x_g  - x
            #print("ex",error_x)
            error_y  = y_g  - y
            #print("ey",error_y)

            if((error_x>=-3) and (error_x<=3)):
                error_x = 0
            if((error_y>=-3) and (error_y<=3)):
                error_y = 0
            #print("error_x",error_x)
            #print("error_y",error_y)
                  # get the error in the robot's reference frame
                  # @Xreference//Ycam
            gr_y  = error_x*math.cos(theta)  + error_y*math.sin(theta) #takes rad
            gr_x  = -error_x*math.sin(theta) + error_y*math.cos(theta)

                 # @ Xreference//Xcam  == - eqn elmo3eed
            #gr_x  = -(error_x*math.cos(theta)  + error_y*math.sin(theta)) #takes rad
            #gr_y  = -error_x*math.sin(theta) + error_y*math.cos(theta)

            #print("gr_y",gr_y)
            #print("gr_x",gr_x)

                  # calculate rho and alfa
            rho  = math.sqrt(gr_x**2+gr_y**2) #in cm
            alfa = math.atan2(gr_y,gr_x) #in rad
                  # define controller gains
            K_RHO = 1.4 # 0.6 doesn't work fine with me
                  #(robot becomes unstable a bit after arriving to the desired pose)
            K_ALPHA = 0.5; #K_THETA = 0.5
                  #calculate control commands
            v     = K_RHO*rho       # in cm/sec             # v = linear velocity command
            omega = K_ALPHA*alfa    # in rad/sec            # omega = angular velocity command
                  # return th control commands
            twist = Twist()
            gtg_flag = Byte()
            gtg_flag = 0

            if((omega<=0.2) and (omega>=-0.2)):
                omega = 0;
            if (omega!=0):
                twist.linear.x  = 0; twist.linear.y  = 0; twist.linear.z  = 0;
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = omega;

            elif (omega == 0):
                twist.linear.x  = v; twist.linear.y  = 0; twist.linear.z  = 0;
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0;
            #print("going to publish")
            #print("publishing1")
        cmd_vel_publisher1.publish(twist)
        #cmd_vel_publisher2.publish(gtg_flag)

        if(gr_x==0 and gr_y==0):
            print("flage")
            flage=1
        if(flage==1):
            #print("increment i")
            i-=2
    if i<0:
        twist = Twist()
        gtg_flag = Byte()
        gtg_flag = 1
        twist.linear.x  = 0; twist.linear.y  = 0; twist.linear.z  = 0;
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0;
        print("i",i)
        cmd_vel_publisher1.publish(twist)
        cmd_vel_publisher2.publish(gtg_flag)

if __name__ == '__main__':
    try:
        gtg_talker()
    except rospy.ROSInterruptException:
        pass
    finally:
        rospy.loginfo("%s closed" % rospy.get_name())
