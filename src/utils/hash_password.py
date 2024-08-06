import bcrypt
import jwt
from settings import Settings

def hash_password(password : str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(password :str, hashed_password : bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_access_token(user_id: int) -> str:
    payload = {'user_id': user_id}
    access_token = jwt.encode(payload, Settings.SECRET_KEY, algorithm='HS256')

    return access_token