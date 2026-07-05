import os

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")


def create_demo_checkout_url(business, booking):
    """Demo mode stand-in for a real gateway checkout URL. Points to our own
    in-app payment simulation page instead of an external provider.

    To go live later: swap the call site in bookings.py back to
    app/utils/dpo_client.py's create_payment_token(), which is already built
    and just needs a registered-business DPO account to activate.
    """
    return f"{FRONTEND_URL}/book/{business.slug}/pay/{booking.id}"
