import json, os, env
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
import configparser
from helpers import sign_in_with_email_and_password, print_pretty

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

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Ensure username was submitted
        if not request.form.get("email"):
            return render_template("login.html", msg="Email is needed")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", msg="Password is needed")
            
        try:
            user = sign_in_with_email_and_password(
                api_key, email, password, config)
            session['usr'] = email
            print('---- sign_in_with_email_and_password -----')
            print_pretty(user)
            return redirect(url_for('index'))
        except:
            return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")
    else:
        return render_template("login.html", msg="")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    session.clear()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("signin.html", msg="Must provide username")
        
        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("signin.html", msg="Must provide email")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("signin.html", msg="Must provide password")

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation_password"):
            return render_template("signin.html", msg="Must provide confirmation")
        
        elif not request.form.get("password") == request.form.get("confirmation"):
             return render_template("signin.html", msg="Must password and confirmation match")

        user = auth.create_user(
        email= email,
        email_verified=False,
        password= password,
        display_name= username,
        disabled=False)

        print(f'{username}\'s account is successfly created')
        session['usr'] = user.email
        return redirect(url_for('index'), code=200)
    else:
        return render_template("signin.html", msg="")


@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('qfb_tokyo'), code=200)
    user = auth.get_user_by_email(usr)
    return render_template("index.html", user=user.display_name)

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("reset.html", msg="Must provide email")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("reset.html", msg="Must provide password")
        
        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation_password"):
            return render_template("reset.html", msg="Must provide confirmation")
        
        elif not request.form.get("password") == request.form.get("confirmation_password"):
             return render_template("reset.html", msg="Must password and confirmation match")

        uid = auth.get_user_by_email(email).uid
        user = auth.update_user(
            uid,
            email=email,
            password=password
            )

        print(f'{user.display_name}\'s account is successfly updated')
        session['usr'] = email
        return redirect(url_for('index'))
    else:
        return render_template("reset.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('qfb_tokyo'))


if __name__ == "__main__":
    app.run(debug=True)
