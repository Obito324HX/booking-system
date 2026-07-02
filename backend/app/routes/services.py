from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Business, Service, Staff, Availability, Booking

services_bp = Blueprint("services", __name__)


# ---- Public: list services for a business (by slug) ----
@services_bp.get("/businesses/<slug>/services")
def list_services(slug):
    business = Business.query.filter_by(slug=slug).first()
    if not business:
        return jsonify({"error": "Business not found"}), 404
    services = Service.query.filter_by(business_id=business.id, active=True).all()
    return jsonify([s.to_dict() for s in services])


# ---- Public: available slots for a given service + date ----
@services_bp.get("/businesses/<slug>/availability")
def get_availability(slug):
    business = Business.query.filter_by(slug=slug).first()
    if not business:
        return jsonify({"error": "Business not found"}), 404

    service_id = request.args.get("service_id")
    date_str = request.args.get("date")  # YYYY-MM-DD
    if not service_id or not date_str:
        return jsonify({"error": "service_id and date are required"}), 400

    service = Service.query.get(service_id)
    if not service or service.business_id != business.id:
        return jsonify({"error": "Service not found"}), 404

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    day_of_week = target_date.weekday()  # 0=Monday

    windows = Availability.query.filter_by(business_id=business.id, day_of_week=day_of_week).all()
    if not windows:
        return jsonify({"slots": []})

    existing = Booking.query.filter(
        Booking.business_id == business.id,
        Booking.status != "cancelled",
        db.func.date(Booking.booking_time) == target_date,
    ).all()
    booked_times = {b.booking_time for b in existing}

    slots = []
    duration = timedelta(minutes=service.duration_minutes)
    for window in windows:
        current = datetime.combine(target_date, window.start_time)
        end = datetime.combine(target_date, window.end_time)
        while current + duration <= end:
            if current not in booked_times:
                slots.append(current.strftime("%H:%M"))
            current += duration

    return jsonify({"slots": slots})


# ---- Owner (authenticated): manage services ----
@services_bp.get("/services")
@jwt_required()
def list_my_services():
    business_id = get_jwt_identity()
    services = Service.query.filter_by(business_id=business_id).all()
    return jsonify([s.to_dict() for s in services])


@services_bp.post("/services")
@jwt_required()
def create_service():
    business_id = get_jwt_identity()
    data = request.get_json()
    if not data.get("name") or not data.get("price"):
        return jsonify({"error": "name and price are required"}), 400

    service = Service(
        business_id=business_id,
        name=data["name"],
        duration_minutes=data.get("durationMinutes", 30),
        price=data["price"],
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201


@services_bp.patch("/services/<service_id>")
@jwt_required()
def update_service(service_id):
    business_id = get_jwt_identity()
    service = Service.query.get(service_id)
    if not service or service.business_id != business_id:
        return jsonify({"error": "Service not found"}), 404

    data = request.get_json()
    for field, attr in [("name", "name"), ("durationMinutes", "duration_minutes"),
                         ("price", "price"), ("active", "active")]:
        if field in data:
            setattr(service, attr, data[field])
    db.session.commit()
    return jsonify(service.to_dict())


@services_bp.delete("/services/<service_id>")
@jwt_required()
def delete_service(service_id):
    business_id = get_jwt_identity()
    service = Service.query.get(service_id)
    if not service or service.business_id != business_id:
        return jsonify({"error": "Service not found"}), 404
    db.session.delete(service)
    db.session.commit()
    return "", 204


# ---- Owner: manage weekly availability ----
@services_bp.post("/availability")
@jwt_required()
def set_availability():
    business_id = get_jwt_identity()
    data = request.get_json()

    slot = Availability(
        business_id=business_id,
        staff_id=data.get("staffId"),
        day_of_week=data["dayOfWeek"],
        start_time=datetime.strptime(data["startTime"], "%H:%M").time(),
        end_time=datetime.strptime(data["endTime"], "%H:%M").time(),
    )
    db.session.add(slot)
    db.session.commit()
    return jsonify(slot.to_dict()), 201


@services_bp.get("/availability")
@jwt_required()
def list_availability():
    business_id = get_jwt_identity()
    windows = Availability.query.filter_by(business_id=business_id).all()
    return jsonify([w.to_dict() for w in windows])
