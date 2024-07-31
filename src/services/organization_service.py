from src.models import Organization
from database import db

class OrganizationService:
    
    
    def create_organization(org_data : object) -> Organization:
        organization = Organization(org_data)
        db.session.add(organization)
        return organization
    
    
    def get_all() -> list[Organization]:
        organizations = Organization.query.all()
        return organizations
    
    def edit_organization(organization_id: int, organization_data:dict) -> None:
        Organization.query.filter_by(id=organization_id).update(organization_data)
        db.session.commit()