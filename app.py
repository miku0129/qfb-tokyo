import json, os, env, sys
import requests

import tkinter as tk

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
import configparser
from helpers import sign_in_with_email_and_password, print_pretty, update_status_of_books_and_book_shelf, en_key, de_key


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
            return render_template("login.html", msg="Sorry for this failure. Please message to the organizer if this error continue")
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
            return render_template("signin.html", msg="Provide username")
        
        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template("signin.html", msg="Provide email")
        
        # Ensure email hasn't been used 
        try:
            auth.get_user_by_email(email)
            return render_template("signin.html", msg="That email is already resistered. Please log in from login page.")
        except firebase_admin.exceptions.FirebaseError:
            print("This email is able to use for resistration")

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("signin.html", msg="Provide password")
        
        # Ensure password is bigger than 6 characters 
        elif len(password) < 6:
            return render_template("signin.html", msg="Password must be a string at least 6 characters long")

        # Ensure confirmation password was submitted
        if not request.form.get("confirmation_password"):
            return render_template("signin.html", msg="Provide confirmation password")
        
        elif not request.form.get("password") == request.form.get("confirmation_password"):
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

    # update 'books' and 'book_shelf' with vote/unvote
    if request.method == 'POST':
        # data from ajax event 
        book_title = request.form['val'] 

        book_shelf_ref = db.collection(u'book_shelf').document(u'{}'.format(user.uid))
        collection_of_bookshelf = book_shelf_ref.get()
        collection_bookshelf_dict = collection_of_bookshelf.to_dict()
        # if user has 'book_shelf', update it 
        if collection_bookshelf_dict:
            for key in collection_bookshelf_dict:
                # collection_dict[key] == 1 : has voted 
                # collection_dict[key] == 0 : hasn't voted or unvoted

                if key == en_key(book_title):
                    books = db.collection('books')
                    docs = books.stream()
                    update_status_of_books_and_book_shelf(db, docs, book_shelf_ref, book_title, collection_bookshelf_dict[key])
                    return redirect(url_for("index"))
                else:
                    continue
        # if user hasn't had 'book_shelf', create it 
        books = db.collection('books')
        docs = books.stream()
        update_status_of_books_and_book_shelf(db, docs, book_shelf_ref, book_title, 0)
        return redirect(url_for("index"))

    # show listed 'books'
    else:
        # 'books'
        books = db.collection('books')
        docs = books.stream()
        # user's 'book_shelf'
        book_shelf_doc = db.collection(u'book_shelf').document(u'{}'.format( user.uid))
        book_shelf_dict = book_shelf_doc.get().to_dict()

        return render_template("index.html", data=[user.display_name, docs, book_shelf_dict])


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
        
        # Ensure password is bigger than 7 characters 
        elif len(password) < 6:
            return render_template("signin.html", msg="Password must be a string at least 6 characters long")
        
        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation_password"):
            return render_template("reset.html", msg="Must provide confirmation password")
        
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
        
        book_title = request.form['book_title'].strip()
        book_author = request.form['book_author'].strip()
        book_summary = request.form['book_summary']
        
        # Ensure book_title was submitted
        if not request.form.get("book_title"):
            return render_template("edit_add.html", msg="Must provide book title", accept="OK")
        
        # Ensure book_title is less than 30 characters 
        elif len(book_title) > 100:
            return render_template("edit_add.html", msg="Book title must be less than 100 characters", accept="OK")

        # Ensure book_author was submitted
        elif not request.form.get("book_author"):
            return render_template("edit_add.html", msg="Must provide author", accept="OK")
        
        # Ensure book_author is less than 30 characters 
        elif len(book_author) > 100:
            return render_template("edit_add.html", msg="Author name must be less than 100 characters", accept="OK")

        # Ensure book_summary was submitted
        elif not request.form.get("book_summary"):
            return render_template("edit_add.html", msg="Make short summary", accept="OK")
        
        # Ensure book_summary is less than 140 characters 
        elif len(book_summary) > 800:
            return render_template("edit_add.html", msg="Summary must be less than 800 characters", accept="OK")
        
        user = auth.get_user_by_email(session['usr'])
        
        data = {"book_title": book_title, "book_author": book_author, "delete_flag": 0, "book_summary": book_summary, "posted_at": firestore.SERVER_TIMESTAMP, "recommended_by": user.display_name, "uid": user.uid,"votes": 0}

        # Ensure the books hasn't been submitted 
        books = db.collection('books')
        docs = books.stream()
        for doc in docs: 
            if doc.to_dict()['book_title'] == book_title:
                books = db.collection('books')
                docs = books.stream()
                return render_template("edit_add.html", uid=user.uid, books=docs, msg="The book has been listed", accept="OK")

        doc_ref = db.collection('books').document(book_title)
        doc_ref.set(data)

        books = db.collection('books')
        docs = books.stream()
        return render_template('edit_add.html', uid=user.uid, books=docs, msg="The book is successfully listed", accept="OK")

    else:
        uid= auth.get_user_by_email(session['usr']).uid
        books = db.collection('books')
        docs = books.stream()
        return render_template('edit_add.html', uid=uid, books=docs)

@app.route('/edit_delete', methods=['GET', 'POST'])
def edit_delete():
        if request.method == 'POST':
            
            delete_book = request.form['delete_book'].strip()

            uid= auth.get_user_by_email(session['usr']).uid

            # Ensure book_title was submitted
            if not request.form.get("delete_book"):
                return render_template("edit_delete.html", msg="Must provide book title", accept="OK")

            books = db.collection('books')
            docs = books.stream()
            # Ensure the book is existed
            for doc in docs: 
                if doc.to_dict()['book_title'] == delete_book:
                    # Ensure that book was submitted by the user
                    if not doc.to_dict()['uid'] == uid:
                        return render_template("edit_delete.html", uid=uid, books=docs, msg="You can't delete this book", accept="OK")

                    # Delete document in 'books'
                    db.collection('books').document(delete_book).delete()
                    books = db.collection('books')
                    docs = books.stream()
                    # Delete filed in 'book_shelf'
                    book_shelf_ref = db.collection('book_shelf').document(u'{}'.format(uid))
                    book_shelf_ref.update({
                        u'{}'.format(en_key(delete_book)): firestore.DELETE_FIELD})

                    return render_template('edit_delete.html', uid=uid, books=docs, msg="The book is successfully deleted", accept="OK")
                else:
                    continue
            return render_template('edit_delete.html', uid=uid, books=docs, msg="The title is not found", accept="OK")
        else:
            uid= auth.get_user_by_email(session['usr']).uid
            books = db.collection('books')
            docs = books.stream()
            return render_template('edit_delete.html', uid=uid, books=docs)


# show a book list which contain only user had posted 
@app.route('/userlist', methods=['GET', 'POST'])
def show_userlist():

    open_dialog = 'false'
    isDelete = True
    isReport = False

    def openDialog(book):
        root = tk.Tk()

        # メッセージボックスをスクリーン中央に表示
        window_height = 400
        window_width = 500

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # メッセージボックスを最前面に表示
        root.attributes("-topmost", True)
        # ウインドウのタイトルを定義する
        root.title(u'QFB Tokyo')


        #delete the target post
        def deletePost():
            print('target book: ', book)
            print('post is deleted')
            root.destroy()

        def cancelAction():
            print('command is cancled')
            root.destroy()

        
        #close the dialog
        def closeDialog():
            print('dialog is closed')
            root.destroy()

        
        if  isDelete == True:
            #ラベル
            Static1 = tk.Label(text=u'Are you sure you want to delete your post ?')
            Static1.pack()

            #ボタン
            Button_delete = tk.Button(text=u'Delete', width=20, command=lambda:deletePost())
            Button_delete.pack()
            Button_cancel = tk.Button(text=u'Cancel', width=20, command=lambda:cancelAction())
            Button_cancel.pack()


        elif isReport == True:
            Static1 = tk.Label(text=u'Done')
            Static1.pack()

            #ボタン
            Button = tk.Button(text=u'OK', width=50, command=lambda:closeDialog())
            Button.pack()

        root.mainloop()

    if request.method == 'POST':
        book_title = request.form['val']
        open_dialog = request.form['isOpen']

        if open_dialog == 'true':
            openDialog(book_title)
            isDelete = False
            isReport = True
            openDialog(book_title)

        uid= auth.get_user_by_email(session['usr']).uid
        books = db.collection('books')
        docs = books.stream()
        return render_template('userlist.html', uid=uid, books=docs)

    else: 
        uid= auth.get_user_by_email(session['usr']).uid
        books = db.collection('books')
        docs = books.stream()
        return render_template('userlist.html', uid=uid, books=docs)


@app.route('/usage')
def usage():
    return render_template('usage.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('qfb_tokyo'))


if __name__ == "__main__":
    app.run(debug=True)
