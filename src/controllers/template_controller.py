from src.services import TemplateService

class TemplateController:
    
     def get_all():
        try:
            temps = TemplateService.get_all()
            temps = list(map((lambda org: org.to_dict()), temps))
            
            return {'success': True, 'templates': temps}, 200
        except Exception as error:
            return {'success': False, 'error': 'Error getting templates: ' + str(error)}, 500
