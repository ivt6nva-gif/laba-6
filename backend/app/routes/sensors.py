from flask import Blueprint, jsonify, request
from app.db.sensors import sensors_all, sensors_by_location, get_all_measurements_by_sensor, get_measurement_by_sensor_from_to

bp = Blueprint("sensors", __name__, url_prefix="/sensors")

@bp.get("/all")
def all_sensors():
    return jsonify({"data": sensors_all()}), 200

@bp.get("/all/location/<int:location_id>")
def sensors_location(location_id):
    return jsonify({"data": sensors_by_location(location_id)}), 200

@bp.get("/measurements")
def measurements():
    sensor_id = request.args.get("sensor_id", type=int)
    time_from = request.args.get("time_from")
    time_to = request.args.get("time_to")

    if not sensor_id:
        return jsonify({"error": "sensor_id обов'язковий"}), 400

    if time_from and time_to:
        data = get_measurement_by_sensor_from_to(sensor_id, time_from, time_to)
    else:
        data = get_all_measurements_by_sensor(sensor_id)

    return jsonify({"data": data}), 200