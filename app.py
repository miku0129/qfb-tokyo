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
            return render_template("login.html", msg="Sorry for this failure. Please report to the organizer if this error continue")
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
        return redirect(url_for('usage'), code=200)
    else:
        return render_template("signin.html", msg="")


@app.route("/", methods=['GET', 'POST'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('qfb_tokyo'), code=200)

    user = auth.get_user_by_email(usr)

    if request.method == 'POST':
        return render_template("index.html", user=user.display_name)
    else:
        books = db.collection('books')
        docs = books.stream()

        return render_template("index.html", user=user.display_name, books=docs)


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

@app.route('/edit_add', methods=['GET', 'POST'])
def edit_add():
    if request.method == 'POST':
        
        book_title = request.form['book_title']
        book_author = request.form['book_author']
        
        # Ensure book_title was submitted
        if not request.form.get("book_title"):
            return render_template("edit_add.html", msg="Must provide book title")

        # Ensure book_author was submitted
        elif not request.form.get("book_author"):
            return render_template("edit_add.html", msg="Must provide author")
        
        user = auth.get_user_by_email(session['usr'])
        
        data = {"book_title": book_title, "book_author": book_author, "delete_flag": 0, "posted_at": firestore.SERVER_TIMESTAMP, "recommended_by": user.display_name, "uid": user.uid,"votes": 0}

        # Ensure the books hasn't been submitted 
        books = db.collection('books')
        docs = books.stream()
        for doc in docs: 
            if doc.to_dict()['book_title'] == book_title:
                books = db.collection('books')
                docs = books.stream()
                return render_template("edit_add.html", uid=user.uid, books=docs, msg="The book has been listed")

        doc_ref = db.collection('books').document(book_title)
        doc_ref.set(data)

        books = db.collection('books')
        docs = books.stream()
        return render_template('edit_add.html', uid=user.uid, books=docs, msg="The book is successfully listed")

    else:
        uid= auth.get_user_by_email(session['usr']).uid
        books = db.collection('books')
        docs = books.stream()
        return render_template('edit_add.html', uid=uid, books=docs)

@app.route('/edit_delete', methods=['GET', 'POST'])
def edit_delete():
        if request.method == 'POST':
            
            delete_book = request.form['delete_book']

            uid= auth.get_user_by_email(session['usr']).uid

            # Ensure book_title was submitted
            if not request.form.get("delete_book"):
                return render_template("edit_delete.html", msg="Must provide book title")

            books = db.collection('books')
            docs = books.stream()
            # Ensure the book is existed
            for doc in docs: 
                if doc.to_dict()['book_title'] == delete_book:
                    # Ensure that book was submitted by the user
                    if not doc.to_dict()['uid'] == uid:
                        return render_template("edit_delete.html", uid=uid, books=docs, msg="You can't delete this book")
        
                    db.collection('books').document(delete_book).delete()
                    books = db.collection('books')
                    docs = books.stream()
                    return render_template('edit_delete.html', uid=uid, books=docs, msg="The book is successfully deleted")
                else:
                    continue
            return render_template('edit_delete.html', uid=uid, books=docs, msg="The title is not found")
        else:
            uid= auth.get_user_by_email(session['usr']).uid
            books = db.collection('books')
            docs = books.stream()
            return render_template('edit_delete.html', uid=uid, books=docs)


@app.route('/usage')
def usage():
    return render_template('usage.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('qfb_tokyo'))


if __name__ == "__main__":
    app.run(debug=True)
