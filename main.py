from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
import unittest


#Local Imports
#Init the app function
from app import create_app
#Functions what gets the info from the data base connection
from app.firestore_service import get_users
from app.firestore_service import get_todos


#Init the app 
app = create_app()


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response 

    
@app.route('/hello')
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id

    context = {'user_ip': user_ip,
                'username': username,
                'todos': get_todos(user_id = username),
                }
   

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
    

