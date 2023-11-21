import os
import requests
from app import logger
class MessageService:


    def getMessageData(message_json):
        message_data = message_json['entry'][0]['changes'][0]['value']['messages'][0]    
        message_data['name'] = message_json['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        
        #Message supported, move contents from type index to 'content'
        if message_data['type'] != 'unsupported' :
            message_data['content'] = message_data[message_data['type']]
            del message_data[message_data['type']]
        #Message unsupported, content is title from error
        else:
            logger.info(message_data['errors'])
            message_data['content'] = {'error': message_data['errors'][0]['title']}
            message_data['type'] = 'unsupported'
            del message_data['errors']
        
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