# Booking System - Backend

Flask + SQLAlchemy API for the salon/barbershop booking product.

## Run locally

```bash
pip install -r requirements.txt
python run.py
```

Runs on http://localhost:5000. Uses SQLite by default (`instance/booking.db`).
For Railway/Postgres, set `DATABASE_URL` env var.

## Key endpoints

**Public (client-facing booking page uses these):**
- `GET /api/businesses/<slug>` - business info
- `GET /api/businesses/<slug>/services` - list services
- `GET /api/businesses/<slug>/availability?service_id=X&date=YYYY-MM-DD` - open slots
- `POST /api/businesses/<slug>/bookings` - create a booking

**Owner (needs JWT from login):**
- `POST /api/auth/signup` / `POST /api/auth/login`
- `POST /api/services` / `PATCH /api/services/<id>` / `DELETE /api/services/<id>`
- `POST /api/availability` / `GET /api/availability`
- `GET /api/bookings` - dashboard list
- `PATCH /api/bookings/<id>` - update status (confirm/cancel/complete/no_show)

## WhatsApp reminders

`app/utils/whatsapp.py` currently logs messages instead of sending them.
To go live: sign up for WhatsApp Cloud API (free tier via Meta for Developers),
set `WHATSAPP_ACCESS_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` env vars.

## Next steps for a real reminder job

Booking reminders (24hrs before) need a scheduled task - options:
- A simple cron job hitting a new `/api/send-reminders` endpoint daily
- Railway's cron feature if deploying there (same as EHM)
