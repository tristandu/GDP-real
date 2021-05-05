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
                self.turns=["Left", "Left","END"]
                
            elif self.destination==15:
                self.turns=["Straight", "Right", "Straight", "Straight","END"]
                
            elif self.destination==16:
                self.turns=["Straight","Right","Straight","Right","Left","END"]
                
            elif self.destination==17:
                self.turns=["Right", "Straight","Right","Back","Left","Left","END"]
                
            else:
                rospy.signal_shutdown("Wrong destination")
                
        elif self.start==2:
            if self.destination==14:
                self.turns=["Left","Right","Straight","Straight", "Straight","END"]
                
            elif self.destination==15:
                self.turns=["Straight", "Straight", "Right","Straight","END"]
                
            elif self.destination==16:
                self.turns=["Straight","Right","Left","Straight","Back","Right","Left","Straight","Left","Straight","END"]
                
            elif self.destination==17:
                self.turns=["Straight","Right","Straight", "Straight","END"]
                
            else:
                rospy.signal_shutdown("Wrong destination")
        else:
            rospy.signal_shutdown("Wrong starting node")
        
        self.next_turn=self.turns[0]
        loop_rate=rospy.Rate(20)
        while not rospy.is_shutdown():
            self.fnFunction()
            loop_rate.sleep()
            
    def cbTurnRes(self,msg):
        if len(self.turns)>=1:
            del self.turns[0]
        if self.turns!=[]:
            self.next_turn=self.turns[0]
            
    def cbMode(self,msg):
        if msg.data==3 and self.turns==["END"]:
            rospy.signal_shutdown("Delivery accomplished")
            
    def fnFunction(self):
        self.pub_next_turn.publish(self.next_turn)
        
        
if __name__== '__main__':
    rospy.init_node("path_planning", disable_signals=True)
    node = PathPlanning()
    rospy.spin()
