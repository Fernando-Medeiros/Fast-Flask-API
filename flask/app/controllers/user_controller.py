from flask import Blueprint

user = Blueprint('user', __name__,)

@user.get('/')
def get():
    return 'Hello World'