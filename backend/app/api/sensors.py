
from flask import Blueprint, jsonify, request
from app.db.sensors import (
    sensors_all,
    get_all_measurements_by_sensor,
    get_measurement_by_sensor_from_to,
    sensors_by_location,
)
from datetime import datetime

bp = Blueprint("sensors", __name__, url_prefix="/sensors")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@bp.get("/all")
def all_sensors():
    """Повертає список всіх сенсорів"""
    sensors = sensors_all()
    return jsonify({"data": sensors}), 200


@bp.get("/all/location/<int:location_id>")
def all_sensors_by_location(location_id):
    """Повертає всі сенсори для вказаної локації"""
    sensors = sensors_by_location(location_id)
    return jsonify({"data": sensors}), 200


@bp.get("/measurements/<int:sensor_id>")
def measurements_for_sensor(sensor_id):
    """Повертає всі вимірювання для сенсора (короткий список для підказок)"""
    try:
        data = get_all_measurements_by_sensor(sensor_id)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/measurements")
def measurement_by_sensor_from_to():
    """
    Повертає вимірювання для сенсора за діапазоном дат
    Параметри (query string):
        sensor_id (int) - обов'язковий
        time_from (str) - формат YYYY-MM-DD HH:MM:SS
        time_to (str) - формат YYYY-MM-DD HH:MM:SS
    """
    sensor_id = request.args.get("sensor_id", type=int)
    time_from = request.args.get("time_from")
    time_to = request.args.get("time_to")

    if not sensor_id:
        return jsonify({"error": "Параметр 'sensor_id' є обов'язковим"}), 400

    # Опціональна валідація формату дати
    if time_from:
        try:
            datetime.strptime(time_from, DATETIME_FORMAT)
        except ValueError:
            return jsonify({"error": f"Невірний формат time_from. Використовуйте: {DATETIME_FORMAT}"}), 400

    if time_to:
        try:
            datetime.strptime(time_to, DATETIME_FORMAT)
        except ValueError:
            return jsonify({"error": f"Невірний формат time_to. Використовуйте: {DATETIME_FORMAT}"}), 400

    try:
        if time_from and time_to:
            data = get_measurement_by_sensor_from_to(sensor_id, time_from, time_to)
        else:
            data = get_all_measurements_by_sensor(sensor_id)

        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500