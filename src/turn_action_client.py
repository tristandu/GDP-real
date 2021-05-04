#!/usr/bin/env python
from __future__ import print_function
import rospy 
import actionlib
import line_follower_turtlebot.msg
from std_msgs.msg import String,Int32

class TurnClient():

    def __init__(self):
        self.sub_mode = rospy.Subscriber("/mode", Int32, self.cbMode)
        self.sub_next_turn=rospy.Subscriber("/next_turn",String, self.cbNextTurn)
        self.last_msg = 0
        self.goal=None
        self.client = actionlib.SimpleActionClient('turn_action_server', line_follower_turtlebot.msg.TurnAction)
        self.client.wait_for_server()
        
    def cbNextTurn(self,msg):
        self.goal=self.goal = line_follower_turtlebot.msg.TurnGoal(turn_direction=msg.data)


    def cbMode(self, msg):
        if (msg.data==1 and self.last_msg!=1):
            self.client.send_goal(self.goal)
            self.client.wait_for_result()
            self.res=self.client.get_result()
            try:
                print("Result: "+self.res.result)
            except:
                print("program interrupted before completion", file=sys.stderr)
        self.last_msg=msg.data



if __name__ == '__main__':
    rospy.init_node('turn_action_client')
    node = TurnClient()
    rospy.spin()
