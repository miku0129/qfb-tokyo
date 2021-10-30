import json, os, env
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
import configparser
from helpers import sign_in_with_email_and_password, print_pretty

# email = 'test001@example.com'
# password = 'hogehogehoge'

app = Flask(__name__)

app.secret_key = env.SECRET_KEY

# ===================== Firebase =====================================
# Firebase初期化
creds = credentials.Certificate({
    "type": env.FIREBASE_TYPE,
    "project_id": env.FIREBASE_PROJECT_ID,
    "private_key": env.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
    "client_email": env.FIREBASE_CLIENT_EMAIL,
    "token_uri": env.FIREBASE_TOKEN_URI
})

firebase_admin.initialize_app(creds)
db = firestore.client()
# ====================================================================

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

api_key = env.FIREBASE_TOKEN_API_KEY

config = configparser.ConfigParser()
config.read("./config.ini")


@app.route('/qfb_tokyo', methods=['GET'])
def qfb_tokyo():
    return render_template("qfb_tokyo.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'GET':
        return render_template("login.html", msg="")

    email = request.form['email']
    password = request.form['password']

    try:
        user = sign_in_with_email_and_password(
            api_key, email, password, config)

        session['usr'] = email

        print('---- sign_in_with_email_and_password -----')
        print_pretty(user)
        return redirect(url_for('index'))

    except:
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    session.clear()

    if request.method == 'GET':
        return render_template("signin.html", msg="")
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = auth.create_user(
    email= email,
    email_verified=False,
    password= password,
    display_name= username,
    disabled=False)

    # invalid case 

    print(f'{username}\'s account is successfly created')
    session['usr'] = user.email
    return redirect(url_for('index'), code=200)


@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('qfb_tokyo'), code=200)
    user = auth.get_user_by_email(usr)
    return render_template("index.html", user=user.display_name)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('qfb_tokyo'))


if __name__ == "__main__":
    app.run(debug=True)
