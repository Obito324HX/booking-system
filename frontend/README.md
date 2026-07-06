# Booking System — Frontend

React + Vite client for the booking product: public booking pages, an in-app
demo payment flow, and an owner dashboard.

## Run locally

```bash
npm install
npm run dev
```

Runs on http://localhost:5173. Point it at your backend with a `.env`:
VITE_API_URL=http://localhost:5000/api ## Pages

- `/book/:slug` — public booking page (service → day → time → details → deposit payment)
- `/book/:slug/pay/:bookingId` — demo payment simulation page
- `/login` — owner login
- `/dashboard` — manage bookings, services, availability, and account password

## Build

```bash
npm run build
```

Outputs to `dist/`. Deployed on Vercel with root directory set to `frontend/`.
