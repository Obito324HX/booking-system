import os
import requests
import xml.etree.ElementTree as ET

DPO_COMPANY_TOKEN = os.environ.get("DPO_COMPANY_TOKEN", "")
# DPO's account-specific "service type" code — get this from your DPO dashboard
# (Company Info / Services) or from DPO support after signup. There's no
# universal default; every merchant account has its own.
DPO_SERVICE_TYPE = os.environ.get("DPO_SERVICE_TYPE", "")

# NOTE: DPO's docs consistently reference this as the API endpoint, used for both
# test and live company tokens. If DPO gives you a separate sandbox URL during
# onboarding, override these two in .env instead of editing this file.
DPO_API_URL = os.environ.get("DPO_API_URL", "https://secure.3gdirectpay.com/API/v6/")
DPO_PAY_URL = os.environ.get("DPO_PAY_URL", "https://secure.3gdirectpay.com/payv2.php")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")


def _post_xml(xml_body):
    resp = requests.post(
        DPO_API_URL,
        data=xml_body.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        timeout=20,
    )
    return ET.fromstring(resp.content)


def create_payment_token(business, service, booking):
    """Create a DPO transaction token and return (trans_token, payment_page_url).

    DPO's hosted payment page lets the client choose card or mobile money
    (Airtel/MTN/Zamtel) themselves. DPO appends TransactionToken and CompanyRef
    as query params when it redirects the client back to redirect_url.
    """
    redirect_url = f"{FRONTEND_URL}/book/{business.slug}/success"
    amount = service.deposit_amount()

    xml_body = f"""<?xml version="1.0" encoding="utf-8"?>
<API3G>
    <CompanyToken>{DPO_COMPANY_TOKEN}</CompanyToken>
    <Request>createToken</Request>
    <Transaction>
        <PaymentAmount>{amount:.2f}</PaymentAmount>
        <PaymentCurrency>ZMW</PaymentCurrency>
        <CompanyRef>{booking.id}</CompanyRef>
        <RedirectURL>{redirect_url}</RedirectURL>
        <BackURL>{redirect_url}</BackURL>
        <CompanyRefUnique>0</CompanyRefUnique>
        <PTL>15</PTL>
        <PTLtype>minutes</PTLtype>
        <customerFirstName>{business.name}</customerFirstName>
        <customerPhone>{booking.client_phone}</customerPhone>
        <customerCountry>ZM</customerCountry>
    </Transaction>
    <Services>
        <Service>
            <ServiceType>{DPO_SERVICE_TYPE}</ServiceType>
            <ServiceDescription>Deposit for {service.name} at {business.name}</ServiceDescription>
            <ServiceDate>{booking.created_at.strftime('%Y/%m/%d %H:%M')}</ServiceDate>
        </Service>
    </Services>
</API3G>"""

    root = _post_xml(xml_body)
    result = root.findtext("Result")
    if result != "000":
        raise RuntimeError(root.findtext("ResultExplanation") or "DPO token creation failed")

    trans_token = root.findtext("TransToken")
    payment_url = f"{DPO_PAY_URL}?ID={trans_token}"
    return trans_token, payment_url


def verify_transaction(trans_token):
    """Check a DPO transaction's payment status. Result '000' means paid."""
    xml_body = f"""<?xml version="1.0" encoding="utf-8"?>
<API3G>
    <CompanyToken>{DPO_COMPANY_TOKEN}</CompanyToken>
    <Request>verifyToken</Request>
    <TransactionToken>{trans_token}</TransactionToken>
</API3G>"""

    root = _post_xml(xml_body)
    return {
        "result": root.findtext("Result"),
        "resultExplanation": root.findtext("ResultExplanation"),
        "amount": root.findtext("TransactionAmount"),
        "currency": root.findtext("TransactionCurrency"),
    }
