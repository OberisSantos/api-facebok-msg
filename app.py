import os
from flask import Flask, request
#import requests
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-do-app'

#Função para acessar a API do remetente
#callSendAPI: chamar api do remetente
#senderPsid: Id do remetente
def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCES_TOKEN


@app.route('/', methods=["GET", "POST"])
def home():
    return 'Home'

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='8888',debug=True)
    port  =  int ( os.environ.get ( "PORT" ,  5000 )) 
    app.execute (host = '0.0.0.0' ,  porta = port )