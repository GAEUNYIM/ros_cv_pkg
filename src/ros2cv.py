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

class image_converter:

	def __init__(self):
		self.image_pub = rospy.Publisher("/gaeun/usb_cam/image_raw_2", Image)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/gaeun/usb_cam/image_raw", Image, self.callback)
		# Q. Why the subscriber is defined later than the publisher? No maters?
		self.shots = 1
		
	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)
		
		(rows, cols, channels) = cv_image.shape
		if cols > 60 and rows > 60 :
			cv2.circle(cv_image, (50, 50), 10, 255)
			
		cv2.imshow("Image window", cv_image)
		my_input = cv2.waitKey(3)
		print("my_input:", my_input)
		if my_input != -1:
			shots += 1
			cv2.imwrite('/res/capture' + self.shots + '.jpg', cv_image)
		
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e :
			print(e)
		
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
