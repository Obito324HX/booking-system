# Booking System

A multi-tenant appointment booking platform for service businesses — salons,
clinics, tutors, consultants — with deposit payments built in to cut down on
no-shows.

**Live demo:** https://booking-system-eight-steel.vercel.app/book/zed-forge

![Booking flow screenshot](screenshots/booking-flow.jpeg)

## Why this exists

Most booking demos stop at "pick a time and confirm." Real service businesses
lose money to no-shows, so this one goes further: clients pay a small deposit
to hold their slot, right in the booking flow — no separate invoice, no manual
follow-up.

## Features

- **Multi-tenant** — one platform, many independent businesses, each with
  their own booking page, services, staff, and hours
- **Real-time availability** — slots are computed from weekly hours minus
  existing bookings, with abandoned/unpaid holds auto-released after 15 minutes
- **Deposit payments** — configurable per service (e.g. 20% of price), paid
  before a booking is confirmed. Currently running in demo mode (no real
  charge) with a complete DPO Group integration (card + Airtel/MTN/Zamtel
  mobile money) ready to activate once a merchant account is live
- **WhatsApp confirmations** — clients get notified the moment a booking is paid
- **Owner dashboard** — manage bookings, services, weekly availability, and
  account settings from one place
- **PWA-ready, mobile-first** booking pages

## Screenshots

| Booking a slot | Deposit payment | Confirmation |
|---|---|---|
| ![Booking page](screenshots/booking-page.jpeg) | ![Payment step](screenshots/payment-step.jpeg) | ![Ticket](screenshots/ticket.jpeg) |

## Tech stack

**Backend:** Flask, SQLAlchemy, PostgreSQL (Neon), JWT auth, deployed on Railway
**Frontend:** React, Vite, deployed on Vercel
**Payments:** Demo mode now; DPO Group integration built and ready for a
registered-business account

## Architecture

```
Client books a slot
│
▼
Pending booking created (15-min hold)
│
▼
Deposit payment (demo mode / DPO)
│
▼
Booking confirmed + WhatsApp sent
```

## Running locally

```bash
git clone https://github.com/Obito324HX/booking-system.git
cd booking-system

# Backend
cd backend
pip install -r requirements.txt --break-system-packages
python3 seed.py       # optional demo data
python3 run.py        # http://localhost:5000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev            # http://localhost:5173
```

See [`backend/README.md`](backend/README.md) and
[`frontend/README.md`](frontend/README.md) for full setup details, environment
variables, and API endpoints.

## Roadmap

- Activate live DPO Group payments (card + mobile money) once a registered
  business account is approved
- Real email/WhatsApp reminder scheduling (24hrs before appointment)
- Staff-specific booking (model already supports it; not yet exposed in the UI)

---

Built by [Cletus Bwalya](https://obito324hx.github.io/Portfolio/) — Zed-Forge
