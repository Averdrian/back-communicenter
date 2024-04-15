from src.models import Template



class TemplateService:
    
    def get_all() -> list[Template]:
        organizations = Template.query.all()
        return organizations