import json
import os
import env

import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
import configparser


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


@app.route('/qfb_tokyo', methods=['GET'])
def qfb_tokyo():
    return render_template("qfb_tokyo.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", msg="")

    api_key = env.FIREBASE_TOKEN_API_KEY

    config = configparser.ConfigParser()
    config.read("./config.ini")

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


def sign_in_with_email_and_password(api_key, email, password, config):
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    headers = {"Content-type": "application/json"}
    data = json.dumps({"email": email, "password": password,
                       "returnSecureToken": True})
    proxies, verify = get_proxy(config)

    print("proxies", proxies)
    result = requests.post(url=uri,
                           headers=headers,
                           data=data,
                           proxies=proxies,
                           verify=verify)
    print("result")
    return result.json()


def get_proxy(config):

    verify = True
    proxies = None

    if config["proxy"].getboolean("proxy"):
        proxies = {
            "http": config["proxy"]["http"],
            "https": config["proxy"]["https"]
        }
        verify = False

    return proxies, verify


def print_pretty(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=4,
                     sort_keys=True, separators=(',', ': ')))


@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('qfb_tokyo'))
    return render_template("index.html", usr=usr)


@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('qfb_tokyo'))


if __name__ == "__main__":
    app.run(debug=True)
