from dotenv import load_dotenv
load_dotenv()

import os
SECRET_KEY = os.getenv('sec_key')
FIREBASE_TYPE=os.getenv('firebase_type')
FIREBASE_PROJECT_ID = os.getenv('firebase_project_id')
FIREBASE_PRIVATE_KEY = os.getenv('firebase_private_key')
FIREBASE_CLIENT_EMAIL = os.getenv('firebase_client_email')
FIREBASE_TOKEN_URI = os.getenv('firebase_token_uri')
