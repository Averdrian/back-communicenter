import os
import requests
from app import logger
class MessageService:


    # def getWhatsAppName(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

    # def getPhoneNumber(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    
    # def getWamid(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    
    # def getTimeStamp(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    
    # def getMessageType(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0]['type']
    
    # def getMessageContextWamid(message_data):
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0]['context']['id']
    
    # def getMessageObject(message_data):
    #     message_type = MessageService.getMessageType(message_data)
    #     return message_data['entry'][0]['changes'][0]['value']['messages'][0][message_type]
    
    # def getFileMimeType(message_object):
    #     return message_object['mime_type'] if 'mime_type' in message_object else ''
    
    # def getMediaId(message_object):
    #     return message_object['id']

    def getMessageData(message_json):
        message_data = message_json['entry'][0]['changes'][0]['value']['messages'][0]    
        message_data['name'] = message_json['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

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