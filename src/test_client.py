#! /usr/bin/env python

from __future__ import print_function
import rospy
import actionlib
import line_follower_turtlebot.msg

def turn_client():
    client = actionlib.SimpleActionClient('turn_action_server', line_follower_turtlebot.msg.TurnAction)
    client.wait_for_server()
    goal = line_follower_turtlebot.msg.TurnGoal(turn_direction="Right")
    client.send_goal(goal)
    client.wait_for_result()
    return client.get_result()


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('test_client')
        result = turn_client()
        print("Result:" + result.result)
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
