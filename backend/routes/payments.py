from flask import Blueprint, jsonify

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/api/payments/test", methods=["GET"])
def test_payment():
    return jsonify({"message": "Payments route working!"})
