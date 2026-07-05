import uuid
from datetime import datetime
from app import db


def gen_uuid():
    return str(uuid.uuid4())


class Business(db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(120), nullable=False)
    owner_email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    whatsapp_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    service_type = db.Column(db.String(50))  # salon, barbershop, spa, clinic
    slug = db.Column(db.String(120), unique=True, nullable=False)  # for public booking URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship("Service", backref="business", cascade="all, delete-orphan")
    staff = db.relationship("Staff", backref="business", cascade="all, delete-orphan")
    bookings = db.relationship("Booking", backref="business", cascade="all, delete-orphan")
    availability = db.relationship("Availability", backref="business", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "whatsappNumber": self.whatsapp_number,
            "address": self.address,
            "serviceType": self.service_type,
            "slug": self.slug,
        }


class Staff(db.Model):
    __tablename__ = "staff"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    business_id = db.Column(db.String(36), db.ForeignKey("businesses.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone, "active": self.active}


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    business_id = db.Column(db.String(36), db.ForeignKey("businesses.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    deposit_percent = db.Column(db.Integer, nullable=False, default=20)  # % of price required upfront
    active = db.Column(db.Boolean, default=True)

    def deposit_amount(self):
        return round(float(self.price) * self.deposit_percent / 100, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "durationMinutes": self.duration_minutes,
            "price": float(self.price),
            "depositPercent": self.deposit_percent,
            "depositAmount": self.deposit_amount(),
            "active": self.active,
        }


class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    business_id = db.Column(db.String(36), db.ForeignKey("businesses.id"), nullable=False)
    staff_id = db.Column(db.String(36), db.ForeignKey("staff.id"), nullable=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday .. 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "staffId": self.staff_id,
            "dayOfWeek": self.day_of_week,
            "startTime": self.start_time.strftime("%H:%M"),
            "endTime": self.end_time.strftime("%H:%M"),
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    business_id = db.Column(db.String(36), db.ForeignKey("businesses.id"), nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey("services.id"), nullable=False)
    staff_id = db.Column(db.String(36), db.ForeignKey("staff.id"), nullable=True)

    client_name = db.Column(db.String(120), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)

    booking_time = db.Column(db.DateTime, nullable=False)
    # pending_payment: awaiting checkout completion; confirmed: paid/held; cancelled; completed; no_show
    status = db.Column(db.String(20), default="pending_payment")
    reminder_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment_status = db.Column(db.String(20), default="unpaid")  # unpaid, paid, refunded
    deposit_amount = db.Column(db.Numeric(10, 2), nullable=True)
    flutterwave_tx_ref = db.Column(db.String(255), nullable=True, unique=True)
    flutterwave_transaction_id = db.Column(db.String(255), nullable=True)

    service = db.relationship("Service")
    staff = db.relationship("Staff")

    def to_dict(self):
        return {
            "id": self.id,
            "clientName": self.client_name,
            "clientPhone": self.client_phone,
            "bookingTime": self.booking_time.isoformat(),
            "status": self.status,
            "reminderSent": self.reminder_sent,
            "paymentStatus": self.payment_status,
            "depositAmount": float(self.deposit_amount) if self.deposit_amount is not None else None,
            "service": self.service.to_dict() if self.service else None,
            "staff": self.staff.to_dict() if self.staff else None,
        }
