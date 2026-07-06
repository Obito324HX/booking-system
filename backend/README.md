# Booking System — Backend

Flask + SQLAlchemy API for a multi-tenant appointment booking product.

## Run locally

```bash
pip install -r requirements.txt --break-system-packages
python3 run.py
```

Runs on http://localhost:5000. Uses SQLite by default (`instance/booking.db`).
For production/Postgres (e.g. Neon), set the `DATABASE_URL` env var.

## Seed demo data

```bash
python3 seed.py            # adds a demo business (skips if it already exists)
python3 seed.py --reset    # wipes it and reseeds fresh
```

## Key endpoints

**Public (client-facing booking page uses these):**
- `GET /api/businesses/<slug>` — business info
- `GET /api/businesses/<slug>/services` — list services
- `GET /api/businesses/<slug>/availability?service_id=X&date=YYYY-MM-DD` — open slots
- `POST /api/businesses/<slug>/bookings/checkout` — creates a pending booking and a checkout link for the deposit
- `GET /api/bookings/<id>/public` — booking details for the payment page
- `POST /api/bookings/<id>/demo-pay` — simulates a successful deposit payment (see below)

**Owner (needs JWT from login):**
- `POST /api/auth/signup` / `POST /api/auth/login`
- `PATCH /api/auth/password` — change password
- `POST /api/services` / `PATCH /api/services/<id>` / `DELETE /api/services/<id>`
- `POST /api/availability` / `GET /api/availability`
- `GET /api/bookings` — dashboard list
- `PATCH /api/bookings/<id>` — update status (confirm/cancel/complete/no_show)

## Deposit payments

Clients pay a deposit (set per-service via `depositPercent`) before a booking is
confirmed, so businesses aren't left holding a slot for a no-show. Flow:

1. Client submits booking details → backend creates a `pending_payment` booking and
   returns a checkout URL.
2. Client completes payment.
3. Booking flips to `confirmed` / `payment_status: paid`, and a WhatsApp confirmation fires.

**Current mode: demo payments** (`app/utils/demo_payment.py`) — the checkout URL points
to an in-app page that simulates card/mobile money selection with no real charge. This
keeps the full flow demonstrable without requiring a live, registered-business payment
provider account.

**Ready to go live:** `app/utils/dpo_client.py` is a complete DPO Group integration
(XML `createToken`/`verifyToken` calls, Zambia-market card + mobile money support via
Airtel/MTN/Zamtel) — swap the import in `app/routes/bookings.py` back to it once a
registered DPO merchant account is available. Requires `DPO_COMPANY_TOKEN` and
`DPO_SERVICE_TYPE` env vars from the DPO dashboard.

Pending bookings that never complete payment auto-release their slot after 15 minutes
(see `PENDING_HOLD_MINUTES` in `bookings.py`), so abandoned checkouts don't lock a time
slot forever.

## WhatsApp reminders

`app/utils/whatsapp.py` currently logs messages instead of sending them.
To go live: sign up for WhatsApp Cloud API (free tier via Meta for Developers),
set `WHATSAPP_ACCESS_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` env vars.

## Environment variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Postgres connection string (falls back to local SQLite) |
| `JWT_SECRET_KEY` | Signs owner login tokens |
| `FRONTEND_URL` | Used to build payment redirect URLs |
| `DPO_COMPANY_TOKEN` / `DPO_SERVICE_TYPE` | Only needed once live DPO payments are activated |

## Next steps for a real reminder job

Booking reminders (24hrs before) need a scheduled task — options:
- A simple cron job hitting a new `/api/send-reminders` endpoint daily
- Railway's or Render's built-in cron feature
