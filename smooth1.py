#!/usr/bin/env python  
# Student name: Mohamed Mehrez Said
# Student no.: 201295706
import math
from geometry_msgs.msg import Twist

class SmoothController1:

    def __init__(self,x_goal,y_goal):  # class constructor 
        #(arguments are goal position in global reference frame)
        self.x_g = x_goal
        self.y_g = y_goal
   
    def get_twist(self,x, y, theta):  # (a method) 
        # arguments represent robot pose in global frame
        # get the error in the global reference frame 
        error_x = self.x_g - x
        error_y = self.y_g - y
        # get the error in the robot's reference frame
        # gr_x = R(theta)*[x y]T
        gr_x = error_x*math.cos(theta)+error_y*math.sin(theta)
        gr_y = -error_x*math.sin(theta)+error_y*math.cos(theta)
        # calculate controller commands 
        v     = 1.0*gr_x # v = kv*gr_x linear velocity command ==> kv = 1
        omega = 1.0*gr_y # omega = kw*gr_y angular velocity command ==> kw = 1
        # return the control commands
        twist = Twist()
        twist.linear.x  = v; twist.linear.y  = 0; twist.linear.z  = 0;        
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = omega; 
        return twist      
