#!/usr/bin/env python
import rospy
import rospkg
from std_msgs.msg import String
import sys
from os import path
from monitor_class import Monitor

def node():
    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = rospack.get_path('agribot_monitoring') + "/key/"
    if(not path.exists(key_path)):
        rospy.logerr("[Monitoring node] Key folder not present.")
        return

    monitor = Monitor()
    ret = monitor.initialize_connection_with_firestore(key_path + "agribot-cd437-firebase-adminsdk-ypr8o-5e1109055d.json")
    if(not ret):
        rospy.logerr("[Monitoring node] Bucket does not exist. Initialization failed.")
        return

    rospy.init_node('monitoring_node')

    rate = rospy.Rate(0.1)
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass
