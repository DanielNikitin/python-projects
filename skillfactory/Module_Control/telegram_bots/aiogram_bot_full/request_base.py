import requests

link = 'https://icanhazip.com'
# post если нужна авторизация
# get если нужно просто получить контент
                            #text если нужна html
                            #content если нужны байты, напр картинка/файл
responce = requests.get(link).text
print(responce)