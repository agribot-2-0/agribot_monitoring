#!/usr/bin/env python
from os import path, environ
import rospy
import rospkg
import yaml
from google.api_core import exceptions
from firebase_data_models import FIREBASE_DATA_MODELS
import subscribers_callbacks
import ros_messages
from monitor_class import Monitor


from agribot_common.agribot_parameters import get_parameter


def node():  # pylint: disable=too-many-return-statements, too-many-branches
    rospy.init_node('agribot_monitoring')

    try:
        robot_serial_number = get_parameter('rsn')
        certificate_file = get_parameter('certificate_file')
        certificate_path = get_parameter('certificate_path')
    except ValueError as exception_msg:
        rospy.logerr("[Monitoring] {}".format(exception_msg))
        return

    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = path.join(environ.get('AGRIBOT_HOME'), certificate_path)
    if not path.exists(key_path):
        rospy.logerr("[Monitoring] Key folder not present.")
        return

    monitor = Monitor(robot_serial_number)
    ret = monitor.initialize_connection_with_firestore(
        path.join(key_path, certificate_file))
    if not ret:
        rospy.logerr(
            "[Monitoring] Bucket does not exist. Initialization failed.")
        return

    configs_location = path.join(rospack.get_path('agribot_monitoring'),
                                 "configs")

    config = yaml.load(
        open(path.join(configs_location, 'monitoring_node.yaml')))

    for topic_name, item in config['subscribers'].items():
        try:
            rospy.Subscriber(
                topic_name, getattr(ros_messages, item['ros_msg_type']),
                getattr(subscribers_callbacks, item['ros_callback_name']))
        except AttributeError as my_except:
            rospy.logerr(
                "YAML config file is wrongly formated: {}".format(my_except))
            return

    for topic_name, item in config['subscribers'].items():
        if 'wait_for_message' in item:
            if item['wait_for_message'] is True:
                rospy.logwarn("[Monitoring] Waiting for message '{}'".format(topic_name))
                rospy.wait_for_message(topic_name, getattr(ros_messages, item['ros_msg_type']))

    rate = rospy.Rate(0.1)

    while not rospy.is_shutdown():
        try:
            for firebase_location, item in config['firebase_locations'].items(
            ):
                monitor.write_to_db(str(firebase_location),
                                    FIREBASE_DATA_MODELS[item['data_model']])
        except exceptions.ResourceExhausted as my_except:
            rospy.logerr("[Monitoring] Exeption: {}".format(my_except))
            return
        except KeyError as my_except:
            rospy.logerr(
                "YAML config file is wrongly formated: {}".format(my_except))
            return
        rate.sleep()


if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass
