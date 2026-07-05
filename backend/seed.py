"""Seed the database with a realistic demo salon for portfolio/client demos.

Usage:
    python3 seed.py            # adds demo data (skips if 'glow-salon' already exists)
    python3 seed.py --reset    # wipes 'glow-salon' and its bookings, then reseeds fresh
"""
import sys
from datetime import time
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.models import Business, Service, Staff, Availability, Booking

SLUG = "glow-salon"


def seed():
    app = create_app()
    with app.app_context():
        existing = Business.query.filter_by(slug=SLUG).first()

        if existing and "--reset" in sys.argv:
            Booking.query.filter_by(business_id=existing.id).delete()
            Availability.query.filter_by(business_id=existing.id).delete()
            Staff.query.filter_by(business_id=existing.id).delete()
            Service.query.filter_by(business_id=existing.id).delete()
            db.session.delete(existing)
            db.session.commit()
            existing = None

        if existing:
            print(f"'{SLUG}' already exists — run with --reset to wipe and reseed.")
            print(f"Booking page: http://localhost:5173/book/{SLUG}")
            return

        biz = Business(
            name="Glow Salon",
            owner_email="owner@glowsalon.zm",
            password_hash=generate_password_hash("password123"),
            phone="0977000000",
            whatsapp_number="0977000000",
            address="Cairo Road, Lusaka",
            service_type="salon",
            slug=SLUG,
        )
        db.session.add(biz)
        db.session.commit()

        staff = [
            Staff(business_id=biz.id, name="Mwansa", phone="0977111111"),
            Staff(business_id=biz.id, name="Chanda", phone="0977222222"),
        ]
        db.session.add_all(staff)

        services = [
            # (name, duration_minutes, price, deposit_percent)
            ("Wash & Blow Dry", 30, 120, 20),
            ("Haircut & Style", 45, 250, 20),
            ("Kids Cut (under 12)", 30, 100, 15),
            ("Silk Press", 60, 300, 25),
            ("Cornrows (no extensions)", 90, 350, 25),
            ("Full Braids (with extensions)", 180, 600, 30),
            ("Weave Install", 120, 500, 30),
            ("Gel Manicure", 40, 150, 20),
            ("Pedicure", 45, 180, 20),
        ]
        for name, duration, price, deposit in services:
            db.session.add(Service(
                business_id=biz.id, name=name, duration_minutes=duration,
                price=price, deposit_percent=deposit,
            ))
        db.session.commit()

        # Realistic hours: Mon–Fri full day, Saturday half day, closed Sunday
        weekday_hours = [(0, time(9, 0), time(19, 0)),   # Mon
                          (1, time(9, 0), time(19, 0)),   # Tue
                          (2, time(9, 0), time(19, 0)),   # Wed
                          (3, time(9, 0), time(19, 0)),   # Thu
                          (4, time(9, 0), time(19, 0)),   # Fri
                          (5, time(8, 0), time(15, 0))]   # Sat (half day)
        for day, start, end in weekday_hours:
            db.session.add(Availability(business_id=biz.id, day_of_week=day, start_time=start, end_time=end))
        db.session.commit()

        print("Seeded!")
        print(f"Login:  owner@glowsalon.zm / password123")
        print(f"Booking page: http://localhost:5173/book/{SLUG}")


if __name__ == "__main__":
    seed()
