#!/usr/bin/env python  
# Student name: Mohamed Mehrez Said
# Student no.: 201295706
import math
from geometry_msgs.msg import Twist

class SmoothController2:

    def __init__(self,x_goal,y_goal,th_goal):  # class constructor
        # goal pose in global reference frame 
        self.x_g  = x_goal
        self.y_g  = y_goal  
        self.th_g = th_goal  
  
    def get_twist(self,x, y, theta): 
        # arguments are the robot's pose in the global reference frame
        # get the error in the global reference frame 
        error_x  = self.x_g  - x
        error_y  = self.y_g  - y
        error_th = self.th_g - theta
        # get the error in the robot's reference frame
        gr_x  = error_x*math.cos(theta)  + error_y*math.sin(theta)
        gr_y  = -error_x*math.sin(theta) + error_y*math.cos(theta)
        gr_th = error_th
        # calculate rho and alfa 
        rho  = math.sqrt(gr_x**2+gr_y**2)
        alfa = math.atan2(gr_y,gr_x)
        # define controller gains 
        K_RHO = 0.45 # 0.6 doesn't work fine with me
        #(robot becomes unstable a bit after arriving to the desired pose)
        K_ALPHA = 1.6; K_THETA = 0.3
        # calculate control commands 
        v     = K_RHO*rho                    # v = linear velocity command 
        omega = K_ALPHA*alfa - K_THETA*gr_th # omega = angular velocity command
        # return th control commands
        twist = Twist()
        twist.linear.x  = v; twist.linear.y  = 0; twist.linear.z  = 0;        
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = omega; 
        return twist
