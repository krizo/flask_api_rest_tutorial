from werkzeug.security import safe_str_cmp # safe string compare
from section5.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    userid = payload['identity']
    return User.find_by_id(userid)
