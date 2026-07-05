import re
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.models import Business

auth_bp = Blueprint("auth", __name__)


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug


@auth_bp.post("/signup")
def signup():
    data = request.get_json()
    required = ["name", "email", "password"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "name, email, and password are required"}), 400

    if Business.query.filter_by(owner_email=data["email"]).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    base_slug = slugify(data["name"])
    slug = base_slug
    counter = 1
    while Business.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    business = Business(
        name=data["name"],
        owner_email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        phone=data.get("phone"),
        whatsapp_number=data.get("whatsappNumber", data.get("phone")),
        address=data.get("address"),
        service_type=data.get("serviceType", "salon"),
        slug=slug,
    )
    db.session.add(business)
    db.session.commit()

    token = create_access_token(identity=business.id)
    return jsonify({"token": token, "business": business.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    business = Business.query.filter_by(owner_email=data.get("email")).first()

    if not business or not check_password_hash(business.password_hash, data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=business.id)
    return jsonify({"token": token, "business": business.to_dict()})


@auth_bp.patch("/password")
@jwt_required()
def change_password():
    business_id = get_jwt_identity()
    business = Business.query.get(business_id)
    if not business:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    current_password = data.get("currentPassword", "")
    new_password = data.get("newPassword", "")

    if not check_password_hash(business.password_hash, current_password):
        return jsonify({"error": "Current password is incorrect"}), 401

    if len(new_password) < 8:
        return jsonify({"error": "New password must be at least 8 characters"}), 400

    business.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"success": True})
