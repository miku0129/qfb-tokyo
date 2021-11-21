import json
import requests
from flask import redirect, url_for

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


def update_status_of_books_and_book_shelf(db, docs_of_books, ref, title, hasVote):
    for doc_of_books in docs_of_books:
        if doc_of_books.to_dict()['book_title'] == title:
            if hasVote == 1:
                vote_number = doc_of_books.to_dict()['votes'] - 1; 
                hasVote = 0
            else:
                vote_number = doc_of_books.to_dict()['votes'] + 1; 
                hasVote = 1

            # update 'books'
            db.collection('books').document(title).update({"votes":vote_number})

            # update 'book_shelf'
            ref.set({ u'{}'.format(en_key(title)) : hasVote}, merge=True)
            break
        else:
            continue

def en_key(value):
        return value.replace(' ', ('_'))

def de_key(key):
    return key.replace('_', ' ')