import datetime
import math
from tf.transformations import euler_from_quaternion
from firebase_data_models import FIREBASE_DATA_MODELS
from agribot_msgs.msg import AgribotNavigationManagerResult, AgribotEngineErrorData


def get_position_data(pos_data):
    FIREBASE_DATA_MODELS['pose_data_model']['latitude'] = pos_data.latitude
    FIREBASE_DATA_MODELS['pose_data_model']['longitude'] = pos_data.longitude
    FIREBASE_DATA_MODELS['pose_data_model']['altitude'] = pos_data.altitude
    FIREBASE_DATA_MODELS['pose_data_model'][
        'timestamp'] = datetime.datetime.now()


def get_global_orientation(data):
    orientation_q = data.pose.pose.orientation
    orientation_list = [
        orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w
    ]
    [_, _, yaw] = euler_from_quaternion(orientation_list)

    FIREBASE_DATA_MODELS['pose_data_model']['heading'] = enu_to_neu(yaw)


def enu_to_neu(angle_in_enu):
    return -math.degrees(angle_in_enu - math.pi / 2)


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
    if data.result == AgribotNavigationManagerResult.PATH_COMPLETED:
        FIREBASE_DATA_MODELS['current_task_model']['progress'] = 100
    else:
        FIREBASE_DATA_MODELS['current_task_model']['progress'] = int(
            data.current_waypoint * 100 / data.total_waypoints)


def get_engine_data(data):
    FIREBASE_DATA_MODELS['engine_data_model']['accumulator_voltage'] = round(
        data.accumulator_voltage, 1)
    FIREBASE_DATA_MODELS['engine_data_model'][
        'fuel_temperature'] = data.fuel_temperature
    FIREBASE_DATA_MODELS['engine_data_model']['fuel_level'] = data.fuel_level
    FIREBASE_DATA_MODELS['engine_data_model']['fuel_rate'] = data.fuel_rate
    FIREBASE_DATA_MODELS['engine_data_model'][
        'torque_of_engine'] = data.torque_of_engine
    FIREBASE_DATA_MODELS['engine_data_model']['rpm'] = data.rpm
    FIREBASE_DATA_MODELS['engine_data_model'][
        'timestamp'] = datetime.datetime.now()


def get_engine_error(data):
    FIREBASE_DATA_MODELS['engine_data_model'][
        'error_state'] = engine_state_to_string(data.error_state)
    FIREBASE_DATA_MODELS['engine_data_model'][
        'engine_protection_lamp'] = engine_lamp_to_string(
            data.engine_protection_lamp)
    FIREBASE_DATA_MODELS['engine_data_model'][
        'engine_warning_lamp'] = engine_lamp_to_string(
            data.engine_warning_lamp)
    FIREBASE_DATA_MODELS['engine_data_model'][
        'engine_stop_lamp'] = engine_lamp_to_string(data.engine_stop_lamp)
    FIREBASE_DATA_MODELS['engine_data_model']['occ'] = data.occ
    FIREBASE_DATA_MODELS['engine_data_model']['spn'] = data.spn
    FIREBASE_DATA_MODELS['engine_data_model']['fmi'] = data.fmi
    FIREBASE_DATA_MODELS['engine_data_model'][
        'error_number'] = data.error_number
    FIREBASE_DATA_MODELS['engine_data_model'][
        'error_total_count'] = data.error_total_count


def engine_state_to_string(error_state):
    return {
        AgribotEngineErrorData.ERROR_ACTIVE: u"Error active",
        AgribotEngineErrorData.ERROR_PASSIVE: u"Error passive"
    }[error_state]


def engine_lamp_to_string(engine_lamp):
    return {
        AgribotEngineErrorData.LAMP_OFF: u"Lamp off",
        AgribotEngineErrorData.LAMP_ON: u"Lamp on",
        AgribotEngineErrorData.LAMP_1HZ: u"Lamp flashing 1Hz",
        AgribotEngineErrorData.LAMP_2HZ: u"Lamp flashing 2Hz"
    }[engine_lamp]


def get_hydraulics(data):
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_track_FL'] = data.oil_pressure_track_FL
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_track_FR'] = data.oil_pressure_track_FR
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_track_BL'] = data.oil_pressure_track_BL
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_track_BR'] = data.oil_pressure_track_BR
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_manifold_F'] = data.oil_pressure_manifold_F
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_pressure_manifold_B'] = data.oil_pressure_manifold_B
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_cooler_temperature'] = data.oil_cooler_temperature
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'oil_tank_temperature'] = data.oil_tank_temperature
    FIREBASE_DATA_MODELS['hydraulics_data_model'][
        'timestamp'] = datetime.datetime.now()
