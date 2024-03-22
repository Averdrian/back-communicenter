import os
from flask_login import current_user, login_required

@login_required
def graph_messages_url() -> str:
    return "https://graph.facebook.com/{version}/{phone_id}/messages".format(version=os.getenv('WA_API_VERSION'), phone_id=current_user.organization.wa_phone_id)

@login_required
def base_headers() -> dict:
    return {
        "Authorization": "Bearer {token}".format(token=current_user.organization.wa_api_key),
        "Content-Type": "application/json"
    }

def base_graph_messages_json() -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual"
    }