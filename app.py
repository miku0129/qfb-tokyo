from flask import Flask 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

@app.route('/')
def main():
    # ===================== Firebase =====================================
    # このPythonファイルと同じ階層に認証ファイルを配置して、ファイル名を格納
    JSON_PATH = 'qfb-tokyo-firebase-adminsdk-3sbnu-efcb66a282.json'

    # Firebase初期化
    cred = credentials.Certificate(JSON_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    # ====================================================================

    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    }) 

    result = 'done'
    return result


## おまじない
if __name__ == "__main__":
    main.run(debug=True)