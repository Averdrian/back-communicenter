import os
import requests
from app import db, logger
from src.models import Chat, Message

class MessageService:
        
    #Main function for all received messages
    def messageReceived(message_json):
        
        message_data = MessageService.getMessageData(message_json)
        
        logger.debug(message_data)
        
        chat = Chat.query.filter(Chat.phone == message_data['phone_number']).first()
    
        #If chat does not exist we create it
        if not chat:
            chat = Chat(phone=message_data['phone_number'], whatsapp_name=message_data['name'])
            db.session.add(chat)
            db.session.commit()
        
        #Create message
        message = Message(chat.id, message_data)
        db.session.add(message)        
        db.session.commit()
        
        return message_data
        

    #This functions recieves the raw json from entring messages, and it returns a simplified object with all relevant mesasge data
    def getMessageData(message_json):
                
        message_data = message_json['entry'][0]['changes'][0]['value']['messages'][0]    
        message_data['name'] = message_json['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                
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
                del message_data['content']['emoji']    
            else: #No message found
                message_data['content']['message'] = None
            
            
        #Message unsupported, content is title from error
        else:
            message_data['content'] = {'error': message_data['errors'][0]['title']}
            message_data['type'] = 'unsupported'
            del message_data['errors']
        
        message_data['timestamp'] = int(message_data['timestamp'])
        message_data['phone_number'] = message_data['from']
        message_data['wamid'] = message_data['id']
        del message_data['from']
        del message_data['id']
        

        return message_data


    def getMediaUrl(media_id):
        url = 'https://graph.facebook.com/' + os.getenv('GRAPH_VERSION') + '/' + media_id
        headers =  {'Authorization': 'Bearer ' + os.getenv('WA_API_KEY')}
        return requests.get(url, headers=headers).content
        
    def getMediaImage(media_url):
        headers = {'Authorization': 'Bearer ' + os.getenv('WA_API_KEY')}
        return requests.get(media_url, headers=headers)