import json
import requests

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
