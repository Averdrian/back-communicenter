import os
import requests
from database import db
from src.models import Chat, Message, MessageStatus
from src.events import MessageEvents
from datetime import datetime
from src.utils.messages_utils import base_headers_text, base_headers_media, graph_messages_url, base_graph_messages_json, graph_upload_media_url, graph_get_media_by_id_url
from settings import logger
from typing import List
from settings import PAGE_SIZE
from src.models import ChatStatus
from flask_login import login_required, current_user
import base64

class MessageService:
  
    
    def create_message(message_data : dict) -> Message:
        
        message : Message = Message(message_data)
        db.session.add(message)
        db.session.commit()
        
        return message 
    
    def get_message(message_id : int) -> Message:
        message : Message = Message.query.get_or_404(message_id)
        return message
    
    
    def get_messages(chat : Chat, date: datetime) -> List[Message] | None:
        messages : List[Message] = Message.query.filter_by(chat_id=chat.id).filter(Message.sent_at < date).order_by(Message.sent_at.desc()).limit(PAGE_SIZE).all()
        return messages, len(messages) == PAGE_SIZE
  
    
    def get_message_returning_data(message : Message) -> dict :
        mess_data : dict = message.as_dict()
        
        mess_data['new_chat_status'] = message.chat.status
        mess_data['new_chat_status_name'] = ChatStatus(message.chat.status).name
        
        if message.media_id : 
            url_data : str = requests.get(url=graph_get_media_by_id_url(message.media_id), headers=base_headers_media())
            media_response = requests.get(url=url_data.json()['url'], headers=base_headers_media())
        
            if media_response.status_code == 200:
                # Codificar el contenido binario en base64
                media_base64 = base64.b64encode(media_response.content).decode('utf-8')
                mess_data['media'] = {
                    'content': media_base64,    
                    'mime_type': media_response.headers.get('Content-Type', 'application/octet-stream')
                }
            
        return mess_data

    #This functions recieves the raw json from entring messages, and it returns a simplified object with all relevant mesasge data
    def get_message_data(message_json):
        me_json = message_json['entry'][0]['changes'][0]['value']['messages'][0]
        phone_number_id = message_json['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
        
        message_data = {}
        message_data['organization_phone_id'] = phone_number_id
        message_data['status'] = MessageStatus.DELIVERED.value
        message_data['name'] = message_json['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        message_data['type'] = me_json['type']
        
        #Message supported, move contents from type index to 'content'
        if me_json['type'] != 'unsupported' :
            me_json['content'] = me_json[me_json['type']]
            
            #Set to message all possible index of them 
            if isinstance(me_json['content'], list): #Contacts
                me_json['content'] = me_json['content'][0]                
                message_text = 'Name: ' + me_json['content']['name']['formatted_name'] + ' | Phone: ' + (me_json['content']['phones'][0]['wa_id'] if 'phones' in me_json['content'] else 'UNKNOWN')
                message_data['message'] = message_text
            
            elif 'latitude' in me_json['content']: #Location
                message_temp = "Address{{{addr}}} ".format(addr=me_json['content']['address']) if 'address' in me_json['content'] else ''
                message_temp += "Name{{{name}}} ".format(name=me_json['content']['name']) if 'name' in me_json['content'] else ''
                message_temp += "Url{{{url}}} ".format(url=me_json['content']['url']) if 'url' in me_json['content'] else ''
                message_temp += "Message{{{message}}}".format(message=me_json['content']['message']) if 'message' in me_json['content'] else ''
                message_data['message'] = "{{{latitude},{longitude}}} {message}".format(latitude=me_json['content']['latitude'], longitude=me_json['content']['longitude'], message=message_temp).rstrip()
            
            elif 'body' in me_json['content']: #Message
                message_data['message'] = me_json['content']['body']
            
            elif 'mime_type' in me_json['content']: #Message attached to media types (document, video, photo)
                message_data['message'] = me_json['content']['caption'] if 'caption' in me_json['content'] else None
                message_data['media_id'] = me_json['content']['id']
            
            elif 'emoji' in me_json['content']: #Reaction
                message_data['message'] = me_json['content']['emoji']
                message_data['ref_wamid'] = me_json['content']['message_id']
            
            else: #No message found
                message_data['message'] = None
            
            #The message has a reference to other message
            if 'context' in me_json:
                me_json['ref_wamid'] = me_json['context']['id']
                message_data['ref_wamid'] = me_json['context']['id']

        #Message unsupported, content is title from error
        else:
            message_data['message'] = me_json['errors'][0]['title']
            message_data['type'] = 'unsupported'
            
        message_data['timestamp'] = int(me_json['timestamp'])
        message_data['phone_number'] = me_json['from']
        message_data['wamid'] = me_json['id']
        return message_data


    def get_media_url(media_id):
        url = 'https://graph.facebook.com/' + os.getenv('GRAPH_VERSION') + '/' + media_id
        headers =  {'Authorization': 'Bearer ' + os.getenv('WA_API_KEY')}
        return requests.get(url, headers=headers).content
        
    def get_media_image(media_url):
        headers = {'Authorization': 'Bearer ' + os.getenv('WA_API_KEY')}
        return requests.get(media_url, headers=headers)
    
    
    
    def get_status_data(status_json):
        status = status_json['entry'][0]['changes'][0]['value']['statuses'][0]['status']
        wamid = status_json['entry'][0]['changes'][0]['value']['statuses'][0]['id']
        return status, wamid
    
    
    
    def update_status(wamid, status):
        
        #Get the value of status and the message
        status_int = Message.get_message_status(status)
        message = Message.query.filter_by(wamid = wamid).first()
        
        #If messages exists and the new status is above the previous, we update it
        #Its common that we dont hook the status in order, thats why we make the second condition 
        if message and message.status < status_int:
            message.status = status_int
            db.session.add(message)
            db.session.commit()
            
    def can_send(chat_id):
        chat = Chat.query.get(chat_id)
        return chat.expires_at and datetime.now() < chat.expires_at
    
    def prepare_message_body(message_json):
        if message_json['type'] == 'text':
            ret_json = MessageService._prepare_text_message(message_json)
        elif message_json['type'] in ['image', 'video', 'audio', 'document']:
            ret_json = MessageService._prepare_media_message(message_json)
        
        #Phone number
        chat = Chat.query.get(message_json['chat_id'])
        ret_json['to'] = chat.phone
        
        #The message responds to other
        if 'context' in message_json:
            wamid = Message.query.get(message_json['context']).wamid
            if wamid: ret_json['context'] = {'message_id':wamid}
        return ret_json
    
    @login_required
    def send_message(send_json):
        
        response = requests.post(url=graph_messages_url(), json=send_json, headers=base_headers_text())
        if 'error' in response.json() : raise Exception(response.json()['error']['message'])        
        return response.json()['messages'][0]['id']
    
    def _prepare_text_message(message_json):
        ret_json = base_graph_messages_json()
        ret_json['type'] = 'text'
        ret_json['text'] = {
            "preview_url" : True,
            "body": message_json['message']
        }
        return ret_json
    
    def _prepare_media_message(message_json):
        media_id = MessageService._upload_media(message_json['media'])
        message_json['media_id'] = media_id
        
        ret_json = base_graph_messages_json()
        ret_json['type'] = message_json['type']
        ret_json[message_json['type']] = {
            'id':media_id,
            'caption': message_json['message'] if message_json['message'] else None
        }
            
        return ret_json
        
    def _upload_media(media):
        
        files = {
            'messaging_product': (None, 'whatsapp'),
            'file': (media.filename, media.stream, media.mimetype)
            
        }
        response = requests.post(url=graph_upload_media_url(),
                                 files=files, 
                                 headers=base_headers_media()
                                )
        
        if 'error' in response.json() : raise Exception(response.json()['error']['message'])        
        return response.json()['id']