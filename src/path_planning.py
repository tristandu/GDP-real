#!/usr/bin/env python
from std_msgs.msg import String,Int32
from line_follower_turtlebot.msg import TurnActionResult
import rospy

class PathPlanning():
    
    def __init__(self):
        self.sub_result=rospy.Subscriber("/turn_action_server/result", TurnActionResult, self.cbTurnRes)
        self.sub_mode=rospy.Subscriber("/mode", Int32, self.cbMode)
        self.pub_next_turn=rospy.Publisher("/next_turn", String, queue_size=5)
        
        self.start=rospy.get_param('~start')
        self.destination = rospy.get_param('~destination')
        
        if self.start==1:
            if self.destination==14:
                self.turns=["Left", "Left"]
                
            elif self.destination==15:
                self.turns=["Straight", "Right", "Straight", "Straight"]
                
            elif self.destination==16:
                self.turns=["Straight","Right","Straight","Right","Left"]
                
            elif self.destination==17:
                self.turns=["Right", "Straight","Right"]
                
            else:
                rospy.signal_shutdown("Wrong destination")
                
        elif self.start==2:
            if self.destination==14:
                self.turns=["Left","Right","Straight","Straight", "Straight"]
                
            elif self.destination==15:
                self.turns=["Straight", "Straight", "Right","Straight"]
                
            elif self.destination==16:
                self.turns=["Straight","Right","Left","Straight"]
                
            elif self.destination==17:
                self.turns=["Right","Right"]
                
            else:
                rospy.signal_shutdown("Wrong destination")
        else:
            rospy.signal_shutdown("Wrong starting node")
        
        self.next_turn=self.turns[0]
        loop_rate=rospy.Rate(5)
        while not rospy.is_shutdown():
            self.fnFunction()
            loop_rate.sleep()
            
    def cbTurnRes(self,msg):
        if len(self.turns)>=1:
            del self.turns[0]
        if self.turns!=[]:
            self.next_turn=self.turns[0]
            
    def cbMode(self,msg):
        if msg.data==1 and self.turns==[]:
            rospy.signal_shutdown("Delivery accomplished")
            
    def fnFunction(self):
        self.pub_next_turn.publish(self.next_turn)
        
        
if __name__== '__main__':
    rospy.init_node("path_planning", disable_signals=True)
    node = PathPlanning()
    rospy.spin()
