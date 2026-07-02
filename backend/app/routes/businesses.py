from flask import Blueprint, jsonify
from app.models.models import Business

businesses_bp = Blueprint("businesses", __name__)


@businesses_bp.get("/<slug>")
def get_business_by_slug(slug):
    """Public endpoint - powers the client-facing booking page."""
    business = Business.query.filter_by(slug=slug).first()
    if not business:
        return jsonify({"error": "Business not found"}), 404
    return jsonify(business.to_dict())
