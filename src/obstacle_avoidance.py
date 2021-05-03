#!/usr/bin/env python
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import rospy


class Obstacle_Avoidance():
    
    def __init__(self):
        self.sub_mode = rospy.Subscriber("/mode", Int32, self.cbMode)
        self.pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    
    def cbMode(self, msg):
        if msg.data==2:
            vel = Twist()       #null velocity, robot not moving
            self.pub_vel.publish(vel)
            
            
    def main(self):
        rospy.spin()
        
        
        
if __name__ == '__main__':
    rospy.init_node('obstacle_avoidance')
    node = Obstacle_Avoidance()
    node.main()
    
    
    
