#!/usr/bin/env python
import rospy 
from std_msgs.msg import Int32MultiArray

rospy.init_node('tester')
pub = rospy.Publisher('/rob1_CurrentPose', Int32MultiArray, queue_size=10)

array = Int32MultiArray()
array.data= [1,2,3]

if __name__ == '__main__':
	while not rospy.is_shutdown():
		pub.publish(array)
	


