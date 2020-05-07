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
from app.firestore_service import todo_put
from app.firestore_service import todo_delete
from app.firestore_service import todo_update

from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm


#Init the app 
app = create_app()


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response 

    
@app.route('/hello', methods = ['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    

    context = {'user_ip': user_ip,
                'username': username,
                'todo_form': todo_form,
                'delete_form': delete_form,
                'update_form': update_form,
                'todos': get_todos(user_id = username),
                }

    if todo_form.validate_on_submit():
        todo_put(user_id = username, description = todo_form.description.data)
        flash('The task was created')

        return redirect(url_for('hello'))
   

    return render_template('hello.html', **context)



@app.route('/todos/delete/<todo_id>', methods = ['POST'])
@login_required
def delete(todo_id):
    user_id = current_user.id
    todo_delete(user_id = user_id, todo_id = todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods = ['POST'])
@login_required
def update(todo_id, done):
    user_id = current_user.id
    todo_update(user_id = user_id, todo_id = todo_id, done = done)
    
    return redirect(url_for('hello'))




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
    

