#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import LaserScan,Image 
from std_msgs.msg import Int32
import cv2, cv_bridge, numpy


class ModeDecision():

    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.cbScan)
        self.sub_image = rospy.Subscriber("/raspicam_node/image", Image, self.cbImage)
	self.pub_mode = rospy.Publisher("/mode", Int32, queue_size=10)

	#variables that store whether there is an obstacle/node or not
	self.obstacle=False
	self.node=False

	loop_rate = rospy.Rate(3) # 10hz
        while not rospy.is_shutdown():
            self.fnFunction()
            loop_rate.sleep()

    
    def cbImage(self,msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        lower_blue = numpy.array([90,100,100])		#Hue of blue is 240 degree, we divide by 2 to normalize for OpenCV
	upper_blue = numpy.array([150,255,255])
        mask = cv2.inRange(hsv,lower_blue,upper_blue)
	

	height, width = mask.shape[:2]
	if cv2.countNonZero(mask)>0.3*height*width:     #if more than 30% of the pixels are blue, it is a node
	    self.node=True
	else:
	    self.node=False


    def cbScan(self,msg):
	thr1=0.5
	
	if msg.ranges[0]<thr1 and msg.ranges[0]!=0.0:

	    self.obstacle=True
	else:
	    self.obstacle=False

    def fnFunction(self):
	
	mode = Int32()

	if self.obstacle:
	    mode.data=2
	
	elif self.node:
	    mode.data=1

	else:
	    mode.data=0

	self.pub_mode.publish(mode)


    def main(self):
        rospy.spin()



if __name__ == '__main__':
    rospy.init_node('mode_decision')
    node = ModeDecision()
    node.main()

	    
