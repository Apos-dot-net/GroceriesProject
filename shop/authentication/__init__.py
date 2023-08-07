from .models import *
from .routes import *
from .. import login_manager


@login_manager.user_loader
def user_loader(user_id):
    if session["user_type"] == "customer":
        return RegisterModel.query.get(user_id)
    elif session["user_type"] == "admin":
        return User.query.get(user_id)
    else:
        raise PermissionError(f"{session['user_type']} is not a valid user")
