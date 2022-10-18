from werkzeug.security import safe_str_cmp
from models.user import UserModel


# these 2 methods would be used to identify and authenticate users
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    use_id = payload['identity']
    return UserModel.find_by_id(use_id)
