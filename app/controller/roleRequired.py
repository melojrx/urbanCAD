from functools import wraps
from flask_login import  current_user
from flask import render_template, session

def roles_required(*roles):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # print('roles', roles)
            # print('session',  session["roles"])
            # print(any(role in session["roles"] for role in roles))
            if not any(role in session["roles"] for role in roles):
                return render_template('erro.html', e='Usuário sem permissão de acesso.')
            return f(*args, **kwargs)

        return wrapper

    return decorator_function