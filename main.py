from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap

import unittest

from app import create_app


app = create_app()

todos = ['Comprar Café ', 'Enviar Solicitud ', 'Entregar Producto']


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response 

    
@app.route('/hello', methods = ['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')


    context = {'user_ip': user_ip,
                'username': username,
                'todos': todos,
                'login_form': login_form}

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))



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
    

