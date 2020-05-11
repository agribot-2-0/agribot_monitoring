#!/usr/bin/env python
import sys
from os import path
import datetime
import rospy
import rospkg
from google.api_core import exceptions
from sensor_msgs.msg import NavSatFix
from monitor_class import Monitor

POSITION = None

def get_position_data(pos_data):
    global POSITION
    POSITION = {
        'latitude' : pos_data.latitude,
        'longitude' : pos_data.longitude,
        'altitude' : pos_data.altitude,
        'timestamp' : datetime.datetime.now()
    }

def node():

    rospy.init_node('monitoring_node')
    if len(sys.argv) < 2:
        rospy.logerr("[Monitoring node] UID not specified.")
        return

    rsn = sys.argv[1]

    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = rospack.get_path('agribot_monitoring') + "/key/"
    if not path.exists(key_path):
        rospy.logerr("[Monitoring node] Key folder not present.")
        return

    monitor = Monitor(rsn)
    ret = monitor.initialize_connection_with_firestore(key_path + "agribot-cd437-" +
                                                       "firebase-adminsdk-ypr8o-5e1109055d.json")
    if not ret:
        rospy.logerr("[Monitoring node] Bucket does not exist. Initialization failed.")
        return

    rospy.Subscriber("agribot/gnss", NavSatFix, get_position_data)
    rate = rospy.Rate(0.1)
    while not rospy.is_shutdown():
        try:
            monitor.write_pose_to_db(POSITION)
        except exceptions.ResourceExhausted as my_except:
            rospy.logerr("[Monitoring node] Exeption: %s" %(my_except))
            break
        rate.sleep()

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass
