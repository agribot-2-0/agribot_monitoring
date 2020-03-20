#!/usr/bin/env python
from os import path
import rospy
import rospkg
from sensor_msgs.msg import NavSatFix
from monitor_class import Monitor

POSITION = None

def get_position_data(pos_data):
    global POSITION
    POSITION = dict(latitude=pos_data.latitude, longitude=pos_data.longitude)

def node():
    rospy.init_node('monitoring_node')
    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = rospack.get_path('agribot_monitoring') + "/key/"
    if not path.exists(key_path):
        rospy.logerr("[Monitoring node] Key folder not present.")
        return

    monitor = Monitor()
    ret = monitor.initialize_connection_with_firestore(key_path + "agribot-cd437-" +
                                                       "firebase-adminsdk-ypr8o-5e1109055d.json")
    if not ret:
        rospy.logerr("[Monitoring node] Bucket does not exist. Initialization failed.")
        return

    rospy.Subscriber("agribot/gnss", NavSatFix, get_position_data)
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        monitor.write_to_db(u'agribot', u'position', POSITION)
        rate.sleep()

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass
