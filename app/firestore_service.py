import firebase_admin 
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {'projectId': 'todos-flask'})

db = firestore.client()

#Functions that get info from the users in the db 

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def get_todos(user_id): 
    return db.collection('users').document(user_id).collection('todos').get()

#Functions to save the user's info in the db

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})
    