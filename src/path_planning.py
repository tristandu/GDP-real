#!/usr/bin/env python
from std_msgs.msg import String,Int32
from line_follower_turtlebot.msg import TurnResult
import rospy

class PathPlanning():
    
    def __init__(self):
        self.sub_result=rospy.Subscriber("/turn_action_server/result", TurnResult, self.cbTurnRes)
        self.sub_mode=rospy.subscriber("/mode", Int32, self.cbMode)
        self.pub_next_turn=rospy.Publisher("/next_turn", String)
        
        self.start=rospy.get_param('~start')
        self.destination = rospy.get_param('~destination')
        self.next_turn=Int32()
        
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
            
        loop_rate=rospy.Rate(5)
        while not rospy.is_shutdown():
            self.fnFunction()
            loop_rate.sleep()
            
    def cbTurnRes(self,msg):
        if self.turns!=[]:
            self.turns.del[0]
            self.next_turn.data=self.turns[0]
            
    def cbMode(self,msg):
        if msg.data==1 and self.turns==[]:
            rospy.signal_shutdown("Delivery accomplished")
            
    def fnFunction(self):
        self.pub_next_turn(self.next_turn)
        
        
if __name__== '__main__':
    rospy.init_mode("path_planning", disable_signals=True)
    node = PathPlanning()
    rospy.spin()
