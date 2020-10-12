#!/usr/bin/env python
import sys
from os import path
import math
import datetime
import rospy
import rospkg
from tf.transformations import euler_from_quaternion

from google.api_core import exceptions
from sensor_msgs.msg import NavSatFix, Imu, Temperature, RelativeHumidity, FluidPressure
from agribot_msgs.msg import AgribotWind
from monitor_class import Monitor

POSITION = {
    'latitude': 0.0,
    'longitude': 0.0,
    'altitude': 0.0,
    'heading': 0.0,
    'timestamp': datetime.datetime.now()
}

TEMPERATURE = {
    'value': 0.0,
    'accuracy': 0.0,
    'timestamp': datetime.datetime.now()
}

HUMIDITY = {
    'value': 0.0,
    'accuracy': 0.0,
    'timestamp': datetime.datetime.now()
}

PRESSURE = {
    'value': 0.0,
    'accuracy': 0.0,
    'timestamp': datetime.datetime.now()
}

WIND = {
    'speed_value': 0.0,
    'speed_accuracy': 0.0,
    'timestamp': datetime.datetime.now()
}


def get_position_data(pos_data):
    POSITION['latitude'] = pos_data.latitude
    POSITION['longitude'] = pos_data.longitude
    POSITION['altitude'] = pos_data.altitude
    POSITION['timestamp'] = datetime.datetime.now()


def get_temperature(data):
    TEMPERATURE['value'] = data.temperature
    TEMPERATURE['accuracy'] = data.variance
    TEMPERATURE['timestamp'] = datetime.datetime.now()


def get_humidity(data):
    HUMIDITY['value'] = data.relative_humidity
    HUMIDITY['accuracy'] = data.variance
    HUMIDITY['timestamp'] = datetime.datetime.now()


def get_pressure(data):
    PRESSURE['value'] = pascals_to_hectopascals(data.fluid_pressure)
    PRESSURE['accuracy'] = data.variance
    PRESSURE['timestamp'] = datetime.datetime.now()


def get_wind(data):
    WIND['speed_value'] = data.average_speed
    WIND['speed_accuracy'] = data.speed_variance
    WIND['timestamp'] = datetime.datetime.now()


def pascals_to_hectopascals(value):
    return value / 100


def get_heading(imu_data):
    orientation_q = imu_data.orientation
    orientation_list = [
        orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w
    ]
    euler = euler_from_quaternion(orientation_list)

    POSITION['heading'] = math.degrees(euler[2])


def node():

    rospy.init_node('monitoring_node')
    if len(sys.argv) < 2:
        rospy.logerr("[Monitoring node] UID not specified.")
        return

    rsn = sys.argv[1]

    # init path handling object:
    rospack = rospkg.RosPack()
    key_path = path.join(rospack.get_path('agribot_monitoring'), "key")
    if not path.exists(key_path):
        rospy.logerr("[Monitoring node] Key folder not present.")
        return

    monitor = Monitor(rsn)
    ret = monitor.initialize_connection_with_firestore(
        path.join(key_path,
                  "agribot-cd437-firebase-adminsdk-ypr8o-5e1109055d.json"))
    if not ret:
        rospy.logerr(
            "[Monitoring node] Bucket does not exist. Initialization failed.")
        return

    rospy.Subscriber("agribot/gnss", NavSatFix, get_position_data)
    rospy.Subscriber("agribot/heading", Imu, get_heading)
    rospy.Subscriber("weather_station/temperature", Temperature,
                     get_temperature)
    rospy.Subscriber("weather_station/humidity", RelativeHumidity,
                     get_humidity)
    rospy.Subscriber("weather_station/atmospheric_pressure", FluidPressure,
                     get_pressure)
    rospy.Subscriber("weather_station/wind_speed", AgribotWind, get_wind)

    rate = rospy.Rate(0.1)

    rospy.wait_for_message('/agribot/gnss', NavSatFix)

    while not rospy.is_shutdown():
        try:
            monitor.write_pose_to_db(POSITION)
            monitor.write_temperature_to_db(TEMPERATURE)
            monitor.write_humidity_to_db(HUMIDITY)
            monitor.write_pressure_to_db(PRESSURE)
            monitor.write_wind_to_db(WIND)
        except exceptions.ResourceExhausted as my_except:
            rospy.logerr("[Monitoring node] Exeption: {}".format(my_except))
            break
        rate.sleep()


if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass
