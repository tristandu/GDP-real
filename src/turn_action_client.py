#!/usr/bin/env python
import rospy, actionlib, line_follower_turtlebot.msg
from std_msgs.msg import Int32

def TurnClient():

    def __init__(self):
        self.sub_mode = rospy.Subscriber("/mode", Int32, self.cbMode)
        self.last_msg = 0
        self.client = actionlib.SimpleActionClient('turn_action_server', line_follower_turtlebot.msg.TurnAction)
        self.client.wait_for_server()


    def cbMode(self, msg):
        if (msg.data==1 and self.last_msg!=1):
            self.goal = line_follower_turtlebot.msg.TurnActionGoal(turn_direction="Right")
            self.client.send_goal(self.goal)
            self.client.wait_for_result()
            self.res=self.client.get_result()
            try:
                print("Result: "+self.res)
            except:
                print("program interrupted before completion", file=sys.stderr)
        self.last_msg=msg.data



if __name__ == '__main__':
    rospy.init_node('turn_action_client')
    node = TurnClient()
    rospy.spin()