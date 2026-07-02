from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Business, Service, Booking
from app.utils.whatsapp import send_booking_confirmation

bookings_bp = Blueprint("bookings", __name__)


# ---- Public: client creates a booking ----
@bookings_bp.post("/businesses/<slug>/bookings")
def create_booking(slug):
    business = Business.query.filter_by(slug=slug).first()
    if not business:
        return jsonify({"error": "Business not found"}), 404

    data = request.get_json()
    required = ["serviceId", "clientName", "clientPhone", "bookingTime"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "serviceId, clientName, clientPhone, and bookingTime are required"}), 400

    service = Service.query.get(data["serviceId"])
    if not service or service.business_id != business.id:
        return jsonify({"error": "Service not found"}), 404

    booking_time = datetime.fromisoformat(data["bookingTime"])

    # prevent double-booking the same slot
    clash = Booking.query.filter_by(
        business_id=business.id, booking_time=booking_time, status="confirmed"
    ).first()
    if clash:
        return jsonify({"error": "This time slot was just booked. Please pick another."}), 409

    booking = Booking(
        business_id=business.id,
        service_id=service.id,
        staff_id=data.get("staffId"),
        client_name=data["clientName"],
        client_phone=data["clientPhone"],
        booking_time=booking_time,
    )
    db.session.add(booking)
    db.session.commit()

    send_booking_confirmation(business, booking)

    return jsonify(booking.to_dict()), 201


# ---- Owner: view all bookings (dashboard) ----
@bookings_bp.get("/bookings")
@jwt_required()
def list_bookings():
    business_id = get_jwt_identity()
    status = request.args.get("status")

    query = Booking.query.filter_by(business_id=business_id)
    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(Booking.booking_time).all()
    return jsonify([b.to_dict() for b in bookings])


# ---- Owner: update booking status (confirm/cancel/complete/no-show) ----
@bookings_bp.patch("/bookings/<booking_id>")
@jwt_required()
def update_booking(booking_id):
    business_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    if not booking or booking.business_id != business_id:
        return jsonify({"error": "Booking not found"}), 404

    data = request.get_json()
    if "status" in data:
        if data["status"] not in ("confirmed", "cancelled", "completed", "no_show"):
            return jsonify({"error": "Invalid status"}), 400
        booking.status = data["status"]

    db.session.commit()
    return jsonify(booking.to_dict())
