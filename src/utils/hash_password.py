import bcrypt
import jwt
import app

def hash_password(password : str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(password :str, hashed_password : bytes):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_access_token(user_id: int):
    payload = {'user_id': user_id}
    access_token = jwt.encode(payload, app.Config.SECRET_KEY, algorithm='HS256')

    return access_token