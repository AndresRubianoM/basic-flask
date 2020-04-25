from flask import render_template, flash, redirect, url_for, session

#Local Imports
from . import auth
from ..forms import LoginForm

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    login_form = LoginForm()
    
    context = {
                'login_form': login_form,
    }

    #Set the info to  write the flash message
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)