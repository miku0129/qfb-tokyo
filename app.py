import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase

import json, os
# import ini
# from dotenv import load_dotenv, dotenv_values


# email = 'test001@example.com'
# password = 'hogehogehoge'

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# config = dotenv_values(".env")
# print(".env", config); 

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# ===================== Firebase =====================================
# このPythonファイルと同じ階層に認証ファイルを配置して、ファイル名を格納
JSON_PATH = 'qfb-tokyo-firebase-adminsdk-3sbnu-efcb66a282.json'

# Firebase初期化
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

with open("firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# ====================================================================


# doc_ref = db.collection(u'users').document(u'alovelace')
# doc_ref.set({
#     u'first': u'Mikke',
#     u'last': u'Lovelace',
#     u'born': 1815
# }) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",msg="")

    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['usr'] = email
        return redirect(url_for('index'))
    except:
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('login'))
    return render_template("index.html", usr=usr)

@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)