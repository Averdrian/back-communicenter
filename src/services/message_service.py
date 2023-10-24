

class MessageService:


    def getWhatsAppName(message_data):
        return message_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

    def getPhoneNumber(message_data):
        return message_data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    
    def getWamid(message_data):
        return message_data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    
    def getTimeStamp(message_data):
        return message_data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    
    def getMessageType(message_data):
        return message_data['entry'][0]['changes'][0]['value']['messages'][0]['type']
    
    def getMessageContextWamid(message_data):
        return message_data['entry'][0]['changes'][0]['value']['messages'][0]['context']['id']
    
    def getMessageObject(message_data):
        message_type = MessageService.getMessageType(message_data)
        return message_data['entry'][0]['changes'][0]['value']['messages'][0][message_type]
    
    def getFileMimeType(message_object):
        return message_object['mime_type'] if 'mime_type' in message_object else None
        