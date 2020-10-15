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
    }
}
