import bcrypt


def hash_password(password : str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(password :str, hashed_password : bytes):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))