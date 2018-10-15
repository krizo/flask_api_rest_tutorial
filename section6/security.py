from werkzeug.security import safe_str_cmp # safe string compare
from section6.models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    userid = payload['identity']
    return UserModel.find_by_id(userid)
