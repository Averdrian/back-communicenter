import os
from flask_login import current_user, login_required

@login_required
def graph_messages_url() -> str:
    return "https://graph.facebook.com/{version}/{phone_id}/messages".format(version=os.getenv('WA_API_VERSION'), phone_id=current_user.organization.wa_phone_id)

@login_required
def graph_upload_media_url() -> str:
    return "https://graph.facebook.com/{version}/{phone_id}/media".format(version=os.getenv('WA_API_VERSION'), phone_id=current_user.organization.wa_phone_id)

@login_required
def graph_get_media_by_id_url(media_id : int) -> str:
    return "https://graph.facebook.com/{version}/{media_id}".format(version=os.getenv('WA_API_VERSION'), media_id=media_id)

@login_required
def base_headers_text() -> dict:
    return {
        "Authorization": "Bearer {token}".format(token=current_user.organization.wa_api_key),
        "Content-Type": "application/json"
    }
    
@login_required
def base_headers_media() -> dict:
    return {
        "Authorization": "Bearer {token}".format(token=current_user.organization.wa_api_key)
    }

@login_required
def base_graph_messages_json() -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual"
    }
    
    
