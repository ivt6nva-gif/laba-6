from flask import Blueprint
bp = Blueprint("health_check", __name__)
@bp.get("/health_check")
def health_check():
    return "Ok"