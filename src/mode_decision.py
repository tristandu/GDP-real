#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import LaserScan,Image 
from std_msgs.msg import Int32
from line_follower_turtlebot.msg import TurnActionGoal,TurnActionResult
import cv2, cv_bridge, numpy


class ModeDecision():

    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.cbScan)
        self.sub_image = rospy.Subscriber("/raspicam_node/image", Image, self.cbImage)
	self.sub_action_start = rospy.Subscriber("/turn_action_server/goal", TurnActionGoal, self.cbGoal)
	self.sub_action_end = rospy.Subscriber("/turn_action_server/result", TurnActionResult, self.cbResult)
	
	self.pub_mode = rospy.Publisher("/mode", Int32, queue_size=10)

	#variables that store whether there is an obstacle/node or not
	self.action_running=False
	self.obstacle=False
	self.node=False

	loop_rate = rospy.Rate(5) # 10hz
        while not rospy.is_shutdown():
            self.fnFunction()
            loop_rate.sleep()
		
		
    def cbGoal(self,msg):
	self.action_running=True
	
    def cbResult(self,msg):
	self.action_running=False
		
    
    def cbImage(self,msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        lower_red1 = numpy.array([0,100,100])		#Hue of blue is 240 degree, we divide by 2 to normalize for OpenCV
	upper_red1 = numpy.array([15,255,255])
	lower_red2 = numpy.array([165,100,100])
	upper_red2 = numpy.array([180,255,255])

        mask1 = cv2.inRange(hsv,lower_red1,upper_red1)
	mask2 = cv2.inRange(hsv,lower_red2,upper_red2)
	mask=mask1+mask2
	

	height, width = mask.shape[:2]
	if cv2.countNonZero(mask)>0.2*height*width:     #if more than 20% of the pixels are blue, it is a node
	    self.node=True
	else:
	    self.node=False


    def cbScan(self,msg):
	thr1=0.3
	
	if (msg.ranges[0]<thr1 and msg.ranges[0]!=0.0) or (msg.ranges[15]<thr1 and msg.ranges[15]!=0.0) or (msg.ranges[345]<thr1 and msg.ranges[345]!=0.0):

	    self.obstacle=True
	else:
	    self.obstacle=False

    def fnFunction(self):
	
	mode = Int32()
	
	if self.action_running:
	    mode.data=3

	elif self.obstacle:
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

	    
