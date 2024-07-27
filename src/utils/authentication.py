from flask_login import current_user
from flask import jsonify
from src.models import UserRole


def manager_required(func):
    @login_required
    def decorate_func(*args, **kwargs):
        if not (_is_manager(current_user) or _is_admin_org(current_user)):
            return jsonify({'error': "User must be manager"})
        else: return func(*args, **kwargs)
    return decorate_func 

def login_required(func):
    def decorate_func(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorate_func

def admin_org_required(func):
    @login_required
    def decorate_func(*args, **kwargs):
        if not _is_admin_org(current_user):
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorate_func


def _is_manager(user):
    return user.role == UserRole.MANAGER.value


def _is_admin_org(user):
    return user.organization.is_admin
   