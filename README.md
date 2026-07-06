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
I want you check my github and tell me if you see any changes


Recognized inability to access repository directly; solicited user documentation
Recognized inability to access repository directly; solicited user documentation
I'm not able to actually check your GitHub directly — my search just returned generic GitHub topic pages, not your specific repo, and my fetch tool won't let me grab a URL that hasn't already turned up in a search or that you haven't pasted for me to fetch first (it's a safeguard against pulling arbitrary pages).

Easiest way to verify: just open https://github.com/Obito324HX/booking-system yourself and check —

Does the README render at the bottom of the repo page with the description, features list, and screenshots showing?
Are the three images actually displaying (not broken image icons)?
If anything looks off (broken images, missing sections), paste a screenshot and I'll fix it.

Tobi@fedora:~/booking-system$ cp /path/to/your/booking-page-image.jpg screenshots/booking-page.jpg
cp /path/to/your/payment-step-image.jpg screenshots/payment-step.jpg
cp /path/to/your/ticket-image.jpg screenshots/ticket.jpg
cp screenshots/booking-page.jpg screenshots/booking-flow.jpg
cp: cannot stat '/path/to/your/booking-page-image.jpg': No such file or directory
cp: cannot stat '/path/to/your/payment-step-image.jpg': No such file or directory
cp: cannot stat '/path/to/your/ticket-image.jpg': No such file or directory
cp: cannot stat 'screenshots/booking-page.jpg': No such file or directory
Tobi@fedora:~/booking-system$ 
they are in downloads but ive named them


Thought for 2s
Thought for 2s
Ah, that was a placeholder for you to fill in — no worries. Let's see what's actually in your Downloads folder:

bash
ls ~/Downloads
Paste that output and I'll give you the exact cp commands with the real filenames.

Tobi@fedora:~/booking-system$ ls ~/Downloads
 3336S21_notes.pdf
'34fa43d034469595fd3d4043927d01da (1).png'
 34fa43d034469595fd3d4043927d01da.png
'Activation Program-1.zip'
'Activation Program.zip'
'application packages.pdf'
 beauty-empire-cover.svg
 beauty-empire-salon-demo.html
 booking-backend.zip
 booking-flow.jpeg
 booking-frontend.zip
 booking-page.jpeg
 booking-system
 brightfutures-cover.svg
 brightfutures-demo
'CamScanner 03-22-2026 16.35.pdf'
 Chooso.png
 Class7.pdf
'Cletus_Bwalya_CV (1).docx'
'Cletus_Bwalya_CV (2).docx'
 Cletus_Bwalya_CV.docx
 Cletus_Bwalya_CV.pdf
'Cletus_Bwalya_Industrial_Attachment_Report (1).docx'
 Cletus_Bwalya_Industrial_Attachment_Report.docx
'Cletus CV.docx'
 cletus.docx
 code-1.116.0-1776214233.el8.x86_64.rpm
'communication skills.pdf'
 d2c8494722fd17ecabaecfe645b933b4.png
 DataComm_Practical_Assignment1_Cletus_Bwalya-2.docx
'data communication and networking.pdf'
'Data communication_Networking Question_Bank.pdf'
 data-communications-and-networks.pdf
'DATA COM PAST PAPER.pdf'
'Descrete math.pdf'
'DISCRETE MATHEMATICS TEST 1..pdf'
'discrete math.pdf'
'Document 6.pdf'
 ehm-cover.svg
 env.example
'files (1).zip'
'files (2).zip'
'files (3).zip'
 files.zip
 freshcuts-cover.svg
 freshcuts-demo
 frontend-api-contract.md
 gitignore
'ICT DIPLOMA.doc'
 ict.pdf
'ICT .pdf'
 image.jpg
 IMG-20250218-WA0014.jpg
 IMG-20250222-WA0013.jpg
 IMG-20250223-WA0045.jpg
 IMG-20260222-WA0021.jpg
 index.html
 Industrial_Attachment_Report-1.docx
 Introduction.docx
'it helpdesk.pdf'
 jarvis.py
'MODULATION TECHNIQUES IN WIRELESS COMMUNICATION.docx'
 netgate-installer-v1.2-RELEASE-amd64.iso
'Network and Data communication .pdf'
 ngo-pitch
 NRC.pdf
 Orchis-theme-2025-04-25.tar.gz
 Orchis-theme-2025-04-25.zip
 org.mozilla.firefox.desktop.download
 Particle-sidebar-grub-themes
 Particle-sidebar-grub-themes.tar.xz
 Particle-window-grub-themes
 Particle-window-grub-themes.tar.xz
 patch_portfolio.py
 payment-step.jpeg
 Portfolio
 recovery-codes.txt
 resonate
 resonate-cover.png
 resonate-cover.svg
 resonate.zip
 Routing_Switching_Assignment1_Cletus_Bwalya-1.docx
 S1
 SAD
 Sets.pdf
 SETUP.md
'structured cabling.pdf'
'STUDENT ATTACHMENT RECORDS (2)zz.xlsx'
 The-OSI-and-TCPIP-Models.pdf
 ticket.jpeg
'Unconfirmed 730205.crdownload'
'VID-20250211-WA0303(1).mp4'
 VID-20250218-WA0094.mp4
'WhatsApp Image 2026-06-07 at 16.16.04.jpeg'
'WhatsApp Image 2026-06-18 at 21.33.38.jpeg'
'WhatsApp Image 2026-06-18 at 21.34.27.jpeg'
'WhatsApp Image 2026-06-18 at 21.35.44.jpeg'
'WhatsApp Image 2026-06-18 at 22.05.35.jpeg'
'WhatsApp Image 2026-06-19 at 18.13.36.jpeg'
'WhatsApp Image 2026-06-19 at 18.35.36.jpeg'
'WhatsApp Image 2026-06-23 at 23.46.42.jpeg'
'WhatsApp Image 2026-06-23 at 23.46.43.jpeg'
'WhatsApp Image 2026-06-23 at 23.46.44.jpeg'
'WhatsApp Image 2026-06-24 at 00.05.56.jpeg'
'WhatsApp Image 2026-07-02 at 19.32.57.jpeg'
'WhatsApp Image 2026-07-02 at 20.14.33.jpeg'
'WhatsApp Image 2026-07-02 at 20.27.54.jpeg'
'WhatsApp Image 2026-07-05 at 17.10.36 (1).jpeg'
'WhatsApp Image 2026-07-05 at 17.10.36.jpeg'
'WhatsApp Scan 2026-02-19 at 16.24.58.pdf'
'WhatsApp Video 2026-06-23 at 23.46.44.mp4'
'WhatsApp Video 2026-06-23 at 23.46.45 (1).mp4'
'WhatsApp Video 2026-06-23 at 23.46.45 (2).mp4'
'WhatsApp Video 2026-06-23 at 23.46.45.mp4'
Tobi@fedora:~/booking-system$

Show more
Found them — booking-page.jpeg, booking-flow.jpeg, payment-step.jpeg, ticket.jpeg are all right there. Note they're .jpeg not .jpg, so let's update the README to match and copy them over:

bash
cd ~/booking-system
mkdir -p screenshots
cp ~/Downloads/booking-page.jpeg screenshots/booking-page.jpeg
cp ~/Downloads/booking-flow.jpeg screenshots/booking-flow.jpeg
cp ~/Downloads/payment-step.jpeg screenshots/payment-step.jpeg
cp ~/Downloads/ticket.jpeg screenshots/ticket.jpeg
Now update the README references from .jpg to .jpeg:

bash
sed -i 's/screenshots\/booking-page\.jpg/screenshots\/booking-page.jpeg/; s/screenshots\/booking-flow\.jpg/screenshots\/booking-flow.jpeg/; s/screenshots\/payment-step\.jpg/screenshots\/payment-step.jpeg/; s/screenshots\/ticket\.jpg/screenshots\/ticket.jpeg/' README.md
Verify it worked:

bash
grep screenshots README.md
You should see all four lines now ending in .jpeg. Paste that output, then we'll commit and push.

Tobi@fedora:~/booking-system$ sed -i 's/screenshots\/booking-page\.jpg/screenshots\/booking-page.jpeg/; s/screenshots\/booking-flow\.jpg/screenshots\/booking-flow.jpeg/; s/screenshots\/payment-step\.jpg/screenshots\/payment-step.jpeg/; s/screenshots\/ticket\.jpg/screenshots\/ticket.jpeg/' README.md
sed: can't read README.md: No such file or directory
Tobi@fedora:~/booking-system$


Recognized missing file and identified solution pathway
Recognized missing file and identified solution pathway
Ah — looks like the README.md creation command from a few steps back never actually got run (we got sidetracked by the Vercel 404 fix and screenshot hunting). Let's create it now, this time with the correct .jpeg extensions from the start:

bash
cat > README.md << 'EOF'
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
