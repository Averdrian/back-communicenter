import os

graph_messages_url = "https://graph.facebook.com/{version}/{phone_id}/messages".format(version=os.getenv('WA_API_VERSION'), phone_id=os.getenv('WA_PHONE_ID'))

base_headers = {
    "Authorization": "Bearer {token}".format(token=os.getenv('WA_API_KEY')),
    "Content-Type": "application/json"
}

base_graph_mesages_json = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual"
}