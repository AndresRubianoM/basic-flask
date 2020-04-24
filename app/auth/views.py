from flask import render_template

#Local Imports
from . import auth
from ..forms import LoginForm

@auth.route('/login')
def login():
    context = {
                'login_form': LoginForm()
    }
    return render_template('login.html', **context)