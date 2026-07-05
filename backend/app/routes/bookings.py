from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Business, Service, Booking
from app.utils.whatsapp import send_booking_confirmation
from app.utils.demo_payment import create_demo_checkout_url

bookings_bp = Blueprint("bookings", __name__)

PENDING_HOLD_MINUTES = 15  # how long a pending_payment booking holds the slot


# ---- Public: client starts a booking -> creates a (demo) checkout link for the deposit ----
@bookings_bp.post("/businesses/<slug>/bookings/checkout")
def create_booking_checkout(slug):
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

    # a slot is taken if it's confirmed (paid), or pending payment within the hold window
    hold_cutoff = datetime.utcnow() - timedelta(minutes=PENDING_HOLD_MINUTES)
    clash = Booking.query.filter(
        Booking.business_id == business.id,
        Booking.booking_time == booking_time,
        db.or_(
            Booking.status == "confirmed",
            db.and_(Booking.status == "pending_payment", Booking.created_at >= hold_cutoff),
        ),
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
        status="pending_payment",
        payment_status="unpaid",
        deposit_amount=service.deposit_amount(),
    )
    db.session.add(booking)
    db.session.commit()

    checkout_url = create_demo_checkout_url(business, booking)
    return jsonify({"checkoutUrl": checkout_url, "bookingId": booking.id}), 201


# ---- Public: the demo payment page reads booking details (amount, service) before "paying" ----
@bookings_bp.get("/bookings/<booking_id>/public")
def get_booking_public(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking.to_dict())


# ---- Public: simulates a successful payment. No real money moves — this is a
# stand-in for a real gateway's webhook/verify step (see app/utils/dpo_client.py
# for the real DPO integration, ready to swap back in once the business's DPO
# account is fully registered and approved). ----
@bookings_bp.post("/bookings/<booking_id>/demo-pay")
def demo_pay_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.payment_status != "paid":
        booking.payment_status = "paid"
        booking.status = "confirmed"
        db.session.commit()

        business = Business.query.get(booking.business_id)
        send_booking_confirmation(business, booking)

    return jsonify(booking.to_dict())


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
