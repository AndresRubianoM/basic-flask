from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


#Local Imports
#blueprint
from . import auth
#form class
from ..forms import LoginForm
#Conntection to the db
from ..firestore_service import get_user, user_put
#Classes for login user 
from ..models import UserData, UserModel

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    #Create the instance of the login form 
    login_form = LoginForm()
    
    context = {
                'login_form': login_form,
    }

    #Validates the information from the login form
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            
            
            if check_password_hash(password_from_db, password):
                #user_data = UserData(username, password)
                #user = UserModel(user_data)
                user = UserModel.query(username)
                
                login_user(user)

                flash('Welcome Again')

                return redirect(url_for('index'))
            else:
                flash('The password is wrong')

        else:
            flash('The user youre looking for doesnt exists')

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Welcome!!!')

            return redirect(url_for('hello'))
        
        else:
            flash('That username already exists')



    return render_template('signup.html', **context)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Comeback')
    return redirect(url_for('auth.login'))
