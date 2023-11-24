import os
import requests
from app import db, logger
from src.models import Chat, Message, MessageStatus
from src.events import MessageEvents
from datetime import datetime
from src.utils.messages_utils import base_headers, graph_messages_url, base_graph_mesages_json

class MessageService:
  
    
    def create_message_webhook(chat_id, message_data):
        
        message = Message(chat_id, message_data)
        db.session.add(message)
        db.session.commit()
        MessageEvents.inserted(message)
        
        return message
        
    def create_or_update_chat(message_data):
        chat = Chat.query.filter(Chat.phone == message_data['phone_number']).first()
    
        #If chat does not exist we create it
        if not chat:
            chat = Chat(phone=message_data['phone_number'], whatsapp_name=message_data['name'])
            db.session.add(chat)
            db.session.commit()
        return chat
    
    

    #This functions recieves the raw json from entring messages, and it returns a simplified object with all relevant mesasge data
    def get_message_data(message_json):
        
        message_data = message_json['entry'][0]['changes'][0]['value']['messages'][0]    
        message_data['name'] = message_json['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        message_data['status'] = MessageStatus.DELIVERED.value
        
        #Message supported, move contents from type index to 'content'
        if message_data['type'] != 'unsupported' :
            message_data['content'] = message_data[message_data['type']]
            del message_data[message_data['type']]            
            
            #Set to message all possible index of them 
            if isinstance(message_data['content'], list): #Contacts
                message_data['content'] = message_data['content'][0]
                message_text = 'Name: ' + message_data['content']['name']['formatted_name'] + ' | Phone: ' + message_data['content']['phones'][0]['wa_id']
                message_data['content']['message'] = message_text
            
            elif 'latitude' in message_data['content']: #Location
                message_temp = "Address{{{addr}}} ".format(addr=message_data['content']['address']) if 'address' in message_data['content'] else ''
                message_temp += "Name{{{name}}} ".format(name=message_data['content']['name']) if 'name' in message_data['content'] else ''
                message_temp += "Url{{{url}}} ".format(url=message_data['content']['url']) if 'url' in message_data['content'] else ''
                message_temp += "Message{{{message}}}".format(message=message_data['content']['message']) if 'message' in message_data['content'] else ''
                message_data['content']['message'] =  "{{{latitude},{longitude}}} {message}".format(latitude=message_data['content']['latitude'], longitude=message_data['content']['longitude'], message=message_temp).rstrip()
            
            elif 'body' in message_data['content']: #Message
                message_data['content']['message'] = message_data['content']['body']
                del message_data['content']['body']
            
            elif 'caption' in message_data['content']: #Message attached to media types (document, video, photo)
                message_data['content']['message'] = message_data['content']['caption']
                del message_data['content']['caption']
                
            elif 'emoji' in message_data['content']: #Reaction
                message_data['content']['message'] = message_data['content']['emoji'] 
                message_data['ref_wamid'] = message_data['content']['message_id']
                del message_data['content']['emoji']    
            else: #No message found
                message_data['content']['message'] = None
        
            #The message has a reference to other message
            if 'context' in message_data:
                message_data['ref_wamid'] = message_data['context']['id']
                

        #Message unsupported, content is title from error
        else:
            message_data['content'] = {'message': message_data['errors'][0]['title']}
            message_data['type'] = 'unsupported'
            del message_data['errors']
        
        message_data['timestamp'] = int(message_data['timestamp'])
        message_data['phone_number'] = message_data['from']
        message_data['wamid'] = message_data['id']
        del message_data['from']
        del message_data['id']
        

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
            
    def can_send(message_json):
        chat = Chat.query.get(message_json['chat_id'])
        return chat.expires_at and datetime.now() < chat.expires_at
    
    def prepare_message_body(message_json):
        if message_json['type'] == 'text':
            ret_json = MessageService._prepare_text_message(message_json) 
        elif message_json['type'] == 'media':
            ret_json = base_graph_mesages_json.copy() #TODO: Media messages
        
        #Phone number
        chat = Chat.query.get(message_json['chat_id'])
        ret_json['to'] = chat.phone
        
        # logger.debug(message_json)
        logger.debug('context' in message_json)
        
        #The message responds to other
        if 'context' in message_json:
            logger.info("por que carajo entra")
            wamid = Message.query.get(message_json['context']).wamid
            if wamid: ret_json['context'] = {'message_id':wamid}
        logger.debug(ret_json)
        return ret_json
    
    
    def send_message(send_json):
        response = requests.post(url=graph_messages_url, json=send_json, headers=base_headers)
        if 'error' in response.json() : return False, None
        return True, response.json()['messages'][0]['id']
    
    def _prepare_text_message(message_json):
        logger.info("base graph")
        logger.info(base_graph_mesages_json)
        ret_json = base_graph_mesages_json.copy()
        logger.info("entra _prepare")
        logger.info(ret_json)
        ret_json['type'] = 'text'
        ret_json['text'] = {
            "preview_url" : True,
            "body": message_json['body']
        }
        return ret_json
    
    def create_message_send(message_json, wamid):
        
        message_data = {
                'content':{
                    'message': message_json['body'],
                },
                'user_id' : message_json['user_id'], #TODO: Cuando este bien hecho el auth , tiene que ser el usuario que lo haya creado, o un usuario bot
                'type': message_json['type'],
                'wamid': wamid,
                'timestamp': datetime.now().timestamp()
            }
        
        if 'context' in message_json:
            ref_wamid = Message.query.get(message_json['context']).wamid
            if wamid: message_data['ref_wamid'] = ref_wamid
        
        message = Message(message_json['chat_id'],message_data)
        db.session.add(message)
        db.session.commit()