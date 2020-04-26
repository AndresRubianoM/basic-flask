from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap

import unittest

from app import create_app


from app.firestore_service import get_users
from app.firestore_service import get_todos

app = create_app()



@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response 

    
@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    #login_form = LoginForm()
    username = session.get('username')


    context = {'user_ip': user_ip,
                'username': username,
                'todos': get_todos(user_id = username),
                }

    #if login_form.validate_on_submit():
    #    username = login_form.username.data
    #    session['username'] = username
    #    flash('Nombre de usuario registrado con éxito')

    #    return redirect(url_for('index'))

    users = get_users()

    for user in users:
        print('HEEEEEERRREEEEEE')
        print('user: ', user.id)
        print(user.to_dict()['password'])



    return render_template('hello.html', **context)


#Management of Errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error = error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error = error)

#Command line
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    

