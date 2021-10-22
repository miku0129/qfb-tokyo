from dotenv import load_dotenv
load_dotenv()

import os
SECRET_KEY = os.getenv('sec_key')

JSON_PATH = os.getenv('qfb-tokyo-firebase-adminsdk-3sbnu-efcb66a282.json')
