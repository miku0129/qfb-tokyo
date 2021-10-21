import configparser

ini = configparser.ConfigParser()
ini.read('config.ini', encoding='UTF-8')
print('ini',ini)
ini_key = ini['secret_key']['sec_key']