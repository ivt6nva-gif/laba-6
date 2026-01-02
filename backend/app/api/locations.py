from flask import Blueprint, jsonify
from app.db.locations import location_all

bp = Blueprint("locations", __name__, url_prefix="/locations")

@bp.get("/all")
def get_all_locations():
    locations = location_all()
    return jsonify({"data": locations}), 200