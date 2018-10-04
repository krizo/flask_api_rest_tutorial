from werkzeug.security import safe_str_cmp # safe string compare
from .user import User

users = [
    User(1, 'kriz', 'asdf')
]

username_table = {u.username: u for u in users}
userid_table= {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    userid = payload.get('identity')
    return userid_table.get(userid, None)
