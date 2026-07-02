"""
WhatsApp messaging helper.

For an MVP demo, this just logs the message and builds a wa.me link
(so you can manually verify what would be sent). To go live, plug in
the WhatsApp Cloud API (free tier, Meta-owned) - see notes below.
"""
import os
import logging
import requests

logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")


def send_booking_confirmation(business, booking):
    message = (
        f"Hi {booking.client_name}! Your booking at {business.name} is confirmed:\n"
        f"{booking.service.name} on {booking.booking_time.strftime('%a %d %b, %H:%M')}.\n"
        f"Reply CANCEL to cancel."
    )
    _send_whatsapp(booking.client_phone, message)


def send_reminder(business, booking):
    message = (
        f"Reminder: your appointment at {business.name} "
        f"({booking.service.name}) is tomorrow at {booking.booking_time.strftime('%H:%M')}."
    )
    _send_whatsapp(booking.client_phone, message)


def _send_whatsapp(to_phone, message):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        # Not configured yet - log instead of failing, so booking flow still works
        logger.info("[WhatsApp stub] To: %s | Message: %s", to_phone, message)
        return

    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error("WhatsApp send failed: %s", e)
