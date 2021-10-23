import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase

import json, os
import config

# email = 'test001@example.com'
# password = 'hogehogehoge'

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

# ===================== Firebase =====================================

# Firebase初期化
cred = credentials.Certificate({
    "type":config.FIREBASE_TYPE,
    "project_id": config.FIREBASE_PROJECT_ID,
    "private_key": config.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
    "client_email": config.FIREBASE_CLIENT_EMAIL,
    "token_uri": config.FIREBASE_TOKEN_URI
})
print("cred", cred)
firebase_admin.initialize_app(cred)
db = firestore.client()

# with open("firebaseConfig.json") as f:
#     firebaseConfig = json.loads(f.read())
# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()
# ====================================================================


doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'MMMMY',
    u'last': u'Lovelace',
    u'born': 1815
}) 

@app.route('/', methods=['GET'])
def lp():
    return render_template("lp.html")


# @app.route('/lp', methods=['GET'])
# def lp():
#     return render_template("lp.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template("login.html",msg="")

#     email = request.form['email']
#     password = request.form['password']
#     try:
#         user = auth.sign_in_with_email_and_password(email, password)
#         session['usr'] = email
#         return redirect(url_for('index'))
#     except:
#         return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

# @app.route("/", methods=['GET'])
# def index():
#     usr = session.get('usr')
#     if usr == None:
#         return redirect(url_for('lp'))
#     return render_template("index.html", usr=usr)

# @app.route('/logout')
# def logout():
#     del session['usr']
#     return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)