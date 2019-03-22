#!/usr/bin/env python
import rospy 
from std_msgs.msg import Int32MultiArray

rospy.init_node('tester2')
pub = rospy.Publisher('/goal1', Int32MultiArray, queue_size=10)

array = Int32MultiArray()
array.data= [2,4,5]

if __name__ == '__main__':
	while not rospy.is_shutdown():
		pub.publish(array)
	


