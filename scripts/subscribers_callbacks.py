import datetime
import math
from tf.transformations import euler_from_quaternion
from firebase_data_models import FIREBASE_DATA_MODELS
from agribot_msgs.msg import AgribotMoveBaseMonitorResult


def get_position_data(pos_data):
    FIREBASE_DATA_MODELS['pose_data_model']['latitude'] = pos_data.latitude
    FIREBASE_DATA_MODELS['pose_data_model']['longitude'] = pos_data.longitude
    FIREBASE_DATA_MODELS['pose_data_model']['altitude'] = pos_data.altitude
    FIREBASE_DATA_MODELS['pose_data_model'][
        'timestamp'] = datetime.datetime.now()


def get_heading(imu_data):
    orientation_q = imu_data.orientation
    orientation_list = [
        orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w
    ]
    euler = euler_from_quaternion(orientation_list)

    FIREBASE_DATA_MODELS['pose_data_model']['heading'] = math.degrees(euler[2])


def get_temperature(data):
    FIREBASE_DATA_MODELS['temperature_data_model']['value'] = data.temperature
    FIREBASE_DATA_MODELS['temperature_data_model']['accuracy'] = data.variance
    FIREBASE_DATA_MODELS['temperature_data_model'][
        'timestamp'] = datetime.datetime.now()


def get_humidity(data):
    FIREBASE_DATA_MODELS['humidity_data_model'][
        'value'] = data.relative_humidity
    FIREBASE_DATA_MODELS['humidity_data_model']['accuracy'] = data.variance
    FIREBASE_DATA_MODELS['humidity_data_model'][
        'timestamp'] = datetime.datetime.now()


def get_pressure(data):
    FIREBASE_DATA_MODELS['pressure_data_model'][
        'value'] = pascals_to_hectopascals(data.fluid_pressure)
    FIREBASE_DATA_MODELS['pressure_data_model']['accuracy'] = data.variance
    FIREBASE_DATA_MODELS['pressure_data_model'][
        'timestamp'] = datetime.datetime.now()


# hectopascal is the same as milibar
def pascals_to_hectopascals(value):
    return value / 100


def get_wind(data):
    FIREBASE_DATA_MODELS['wind_data_model']['speed_value'] = data.average_speed
    FIREBASE_DATA_MODELS['wind_data_model'][
        'speed_accuracy'] = data.speed_variance
    FIREBASE_DATA_MODELS['wind_data_model'][
        'timestamp'] = datetime.datetime.now()


# temporarily solution
def current_task_progress(data):
    if data.result == AgribotMoveBaseMonitorResult.PATH_COMPLETED:
        FIREBASE_DATA_MODELS['current_task_model']['progress'] = 100
    else:
        FIREBASE_DATA_MODELS['current_task_model']['progress'] = int(
            data.current_waypoint * 100 / data.total_waypoints)
