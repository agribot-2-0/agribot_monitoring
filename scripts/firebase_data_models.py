import datetime

FIREBASE_DATA_MODELS = {
    "pose_data_model": {
        'latitude': 0.0,
        'longitude': 0.0,
        'altitude': 0.0,
        'heading': 0.0,
        'timestamp': datetime.datetime.now()
    },
    "temperature_data_model": {
        'value': 0.0,
        'accuracy': 0.0,
        'timestamp': datetime.datetime.now()
    },
    "humidity_data_model": {
        'value': 0.0,
        'accuracy': 0.0,
        'timestamp': datetime.datetime.now()
    },
    "pressure_data_model": {
        'value': 0.0,
        'accuracy': 0.0,
        'timestamp': datetime.datetime.now()
    },
    "wind_data_model": {
        'speed_value': 0.0,
        'speed_accuracy': 0.0,
        'timestamp': datetime.datetime.now()
    },
    "current_task_model": {
        'progress': 0
    },
    "hydraulics_data_model": {
        "oil_pressure_track_FL": 0.0,
        "oil_pressure_track_FR": 0.0,
        "oil_pressure_track_BL": 0.0,
        "oil_pressure_track_BR": 0.0,
        "oil_pressure_manifold_F": 0.0,
        "oil_pressure_manifold_B": 0.0,
        "oil_cooler_temperature": 0.0,
        "oil_tank_temperature": 0.0,
        'timestamp': datetime.datetime.now()
    },
    "engine_data_model": {
        "accumulator_voltage": 0.0,
        "fuel_temperature": 0.0,
        "fuel_level": 0.0,
        "fuel_rate": 0.0,
        "torque_of_engine": 0.0,
        "rpm": 0.0,
        "error_state": u"Error passive",
        "engine_protection_lamp": u"Lamp off",
        "engine_warning_lamp": u"Lamp off",
        "engine_stop_lamp": u"Lamp off",
        "occ": 0,
        "spn": 0,
        "fmi": 0,
        "error_number": 0,
        "error_total_count": 0,
        'timestamp': datetime.datetime.now()
    }
}
