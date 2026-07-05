"""Seed the database with Zed-Forge's real booking page.

Usage:
    python3 seed.py            # adds Zed-Forge (skips if it already exists)
    python3 seed.py --reset    # wipes 'zed-forge' and its bookings, then reseeds fresh
"""
import sys
from datetime import time
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.models import Business, Service, Staff, Availability, Booking

SLUG = "zed-forge"


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
            print(f"Booking page: /book/{SLUG}")
            return

        biz = Business(
            name="Zed-Forge",
            owner_email="hello@zedforge.dev",
            password_hash=generate_password_hash("password123"),
            phone="0775580799",
            whatsapp_number="0775580799",
            address="Lusaka, Zambia",
            service_type="web development",
            slug=SLUG,
        )
        db.session.add(biz)
        db.session.commit()

        staff = [Staff(business_id=biz.id, name="Cletus Bwalya", phone="0775580799")]
        db.session.add_all(staff)

        services = [
            # (name, duration_minutes, price, deposit_percent)
            ("Website Consultation Call", 30, 100, 50),
            ("Project Kickoff — Basic Website", 45, 500, 20),
            ("Project Kickoff — Marketplace / Web App", 60, 2000, 20),
            ("Project Kickoff — NGO Portal", 45, 1200, 20),
            ("Project Kickoff — AI Tools Integration", 60, 2500, 20),
            ("Technical Support / Maintenance Session", 30, 150, 30),
        ]
        for name, duration, price, deposit in services:
            db.session.add(Service(
                business_id=biz.id, name=name, duration_minutes=duration,
                price=price, deposit_percent=deposit,
            ))
        db.session.commit()

        # Freelancer hours: Mon–Fri full day, Saturday short window for consults, closed Sunday
        hours = [(0, time(9, 0), time(18, 0)),   # Mon
                 (1, time(9, 0), time(18, 0)),   # Tue
                 (2, time(9, 0), time(18, 0)),   # Wed
                 (3, time(9, 0), time(18, 0)),   # Thu
                 (4, time(9, 0), time(18, 0)),   # Fri
                 (5, time(10, 0), time(14, 0))]  # Sat (short window)
        for day, start, end in hours:
            db.session.add(Availability(business_id=biz.id, day_of_week=day, start_time=start, end_time=end))
        db.session.commit()

        print("Seeded!")
        print(f"Login:  hello@zedforge.dev / password123")
        print(f"Booking page: /book/{SLUG}")


if __name__ == "__main__":
    seed()
