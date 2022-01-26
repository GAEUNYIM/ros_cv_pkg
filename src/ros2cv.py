#!/usr/bin/env python # Check whether the script is excutable
from __future__ import print_function

import roslib
roslib.load_manifest('ros_offboard_sample') # Append the dependencies into PYTHONPATH
import sys
import rospy
import cv2
from std_msgs.msg import String, Int32MultiArray
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty
import os

class image_converter:

	def __init__(self):
		self.shots = 1
		self.image_path = ''
		self.bridge = CvBridge()
		self.image_pub = rospy.Publisher("/gaeun/usb_cam/image_raw_2", Image)
		self.image_sub = rospy.Subscriber("/gaeun/usb_cam/image_raw", Image, self.callback)
		self.reached_signal_sub = rospy.Subscriber("/reached_signal", Empty, self.callback_reached_signal)
		
		
		# Q. Why the subscriber is defined later than the publisher? No maters?
		self.reached_signal = False
		
	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)
		
		(rows, cols, channels) = cv_image.shape
		if cols > 60 and rows > 60 :
			cv2.circle(cv_image, (50, 50), 10, 255)
			
		cv2.imshow("Image window", cv_image)
		cv2.waitKey(3)
		
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e :
			print(e)
			
		# save an image if received signal
		if self.reached_signal == True:
			self.image_path = "/root/catkin_ws/src/ros_cv_pkg/res/saved_image" + str(self.shots) + ".jpeg"
			if (cv2.imwrite(self.image_path, cv_image)): 
				print("LOG::image is saved at " + self.image_path)
			else: 
				print("ERROR::image is not saved well")
			print(os.getcwd())
			self.reached_signal = False
			self.shots += 1

	def callback_reached_signal(self, data):
		print('LOG::callback_reached_signal')
		self.reached_signal = True
		
		
def main(args):
	ic = image_converter()
	rospy.init_node('image_converter', anonymous=True)	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()


	
if	__name__ == '__main__':
	main(sys.argv)
