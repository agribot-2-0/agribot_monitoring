#!/usr/bin/env python
from os import path
import rospy
import rospkg
import yaml
from google.api_core import exceptions
from firebase_data_models import FIREBASE_DATA_MODELS
import subscribers_callbacks
import ros_messages
from monitor_class import Monitor


def if_param_exists(param_name):
    if not rospy.has_param(param_name):
        rospy.logerr("[Monitoring node] '{}' param not set".format(param_name))
        return False
    return True


def node():  # pylint: disable=too-many-return-statements, too-many-branches
    rospy.init_node('agribot_monitoring')
    if if_param_exists('rsn'):
        rsn = rospy.get_param('rsn')
    else:
        return

    if if_param_exists('certificate_repo'):
        certificate_repo = rospy.get_param('certificate_repo')
    else:
        return

    if if_param_exists('certificate_file'):
        certificate_file = rospy.get_param('certificate_file')
    else:
        return

    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = path.join(rospack.get_path(certificate_repo), "key")
    if not path.exists(key_path):
        rospy.logerr("[Monitoring node] Key folder not present.")
        return

    monitor = Monitor(rsn)
    ret = monitor.initialize_connection_with_firestore(
        path.join(key_path, certificate_file))
    if not ret:
        rospy.logerr(
            "[Monitoring node] Bucket does not exist. Initialization failed.")
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

    rate = rospy.Rate(0.1)

    while not rospy.is_shutdown():
        try:
            for firebase_location, item in config['firebase_locations'].items(
            ):
                monitor.write_to_db(str(firebase_location),
                                    FIREBASE_DATA_MODELS[item['data_model']])
        except exceptions.ResourceExhausted as my_except:
            rospy.logerr("[Monitoring node] Exeption: {}".format(my_except))
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
