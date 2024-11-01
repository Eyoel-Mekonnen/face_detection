from flask import Flask, request, jsonify, url_for, redirect, render_template, flash, make_response
from .models.base_models import BaseModel
from .models.user_models import User
from .models.base_models import Base
from werkzeug.security import generate_password_hash
from .models.engine.db_storage import DBStorage
from .models import storage
import jwt
import datetime
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
secret_key = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
#print("I am loading below:")
#print(app.config['SECRET_KEY'])
def register_routes(app):
    
    @app.route('/')
    def home():
        return "Welcome to face recognition attendance system"

    @app.route('/api/register', methods=['POST'])
    def register():

        if request.method == 'POST':
            #data = request.get_json()
            #username = data['username']
            #password = data['password']
            data = request.get_json()
            print("I ma inside the register via direct")
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return jsonify({'error': 'Missing username or password'}), 400

            password_hashed = generate_password_hash(password, method='pbkdf2:sha256')
            #print("MY lenght is")
            #print(len(password_hashed))
            #create an object for the user model which will inherit from basemode
            print(username)
            print(password_hashed)
            user =User(username=username, password_hashed=password_hashed)
            user.save()
            response = redirect('https://localhost:8080/login')
            return response

        else:
            return jsonify({'error': 'Method not allowed'}), 405


    @app.route('/api/login', methods=['POST'])
    def login():
        
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            value = storage.authenticate_user(username, password)
            if value is True:
                #secret_key = app.config['SECRET_KEY']
                print("SECRET_KEY in login:", secret_key, "Type:", type(secret_key))
                #print("SECRET_KEY:", secret_key, "Type:", type(secret_key))
                #print(f"SECRET_KEY: {app.config['SECRET_KEY']} Type: {type(app.config['SECRET_KEY'])}")
                token = jwt.encode({
                    'user': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

                }, app.config['SECRET_KEY'], algorithm="HS256")
                if isinstance(token, bytes):
                    token = token.decode('utf-8')
                #resp = redirect("http://localhost:8501")
                #resp.set_cookie('auth_token', token, httponly=True, secure=False, samesite='Lax')
                #print("Token: {}".format(token))
                return jsonify({'token': token}), 200
            
                #return "You have successuflly logged in."
            else:
                #flash("Incorrect name or Password")
                return jsonify({'message': 'Error Creating token'})
            #possible redirection to streamlit 
        else:
            #return jsonify({'login': 'failed'}), 401
            return jsonify({'message': 'Invalide Username or Password'})

"""
    @app.route('/validate_token', methods=['GET'])
    def validate():
        print("I am inside here mate")
        token = request.cookies.get('auth_token')
        print("TOKEN inside validate {}".format(token))
        if not token:
            return jsonify({"message": "No token provided"}), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return jsonify({"message":"Token is valid"}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
"""
