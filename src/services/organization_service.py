from src.models import Organization
from database import db
from settings import PAGE_SIZE

class OrganizationService:
    
    
    def create_organization(org_data : object) -> Organization:
        organization = Organization(org_data)
        db.session.add(organization)
        return organization
    
    def get_organization(organization_id: int) -> Organization:
        organization = Organization.query.get_or_404(organization_id)
        return organization
    
    def get_all() -> list[Organization]:
        organizations = Organization.query.all()
        return organizations
    
    def edit_organization(organization_id: int, organization_data:dict) -> None:
        Organization.query.filter_by(id=organization_id).update(organization_data)
        db.session.commit()
        
    def get_organizations(page : int):
        organizations_paginated = Organization.query
        organizations_paginated = organizations_paginated.order_by(Organization.name).paginate(page=page, per_page=PAGE_SIZE, error_out=False)
        return [organization.to_dict() for organization in organizations_paginated], organizations_paginated.pages