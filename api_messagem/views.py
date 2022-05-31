from email import message
from django.shortcuts import render

# Create your views here.
import requests
from core import settings
from . import configuracao
import json

SECRET_KEY = "128fea16-bef2-4f86-8402-2fbb9b9ed540e" #chave secreta 



#Função para acessar a API do remetente
#callSendAPI: chamar api do remetente
#senderPsid: Id do remetente
def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN = configuracao.PAGE_ACCES_TOKEN
    
    #carga útil
    payload = {
        'recipient': {'id': senderPsid},
        'message': response,
        'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = "https://graph.facebook.com/v14.0/me/messages?access_token={}".format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)

#Lidar com Mensagem
def handleMessage(senderPsid, receivedMessage): #receivedMessage -> mensagem recebida
    #verificar se contem texto
    if 'text' in receivedMessage:
        #armazenar a resposta
        print(receivedMessage)
        resposta = {'text': 'Você enviou: {}'.format(receivedMessage['text'])}
        callSendAPI(senderPsid, resposta)
    else:
        resposta = {'text': 'Só aceita msg de texto'}
        callSendAPI(senderPsid, resposta)
    


def home(request):
    return render(request, 'home.html', {} )

def indexApi(request):
    if request.method == 'GET':
        VERIFY_TOKEN = SECRET_KEY

        if 'hub.mode' in request:
            mode = request('hub.mode')
            print(mode)

        if 'hub.verify_token' in request:
            token = request.get('hub.verify_token')
            print(token)

        if 'hub.challenge' in request:
            challenge = request.get('hub.challenge')
            print(challenge)
        
        if 'hub.mode' in request and 'hub.verify_token' in request:
            mode = request('hub.mode')
            token = request('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFICADO')

                challenge = request('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403
        
        return 'Algo', 200
    
    if request.method == 'POST':
        VERIFY_TOKEN = SECRET_KEY

        if 'hub.mode' in request:
            mode = request('hub.mode')
            print(mode)

        if 'hub.verify_token' in request:
            token = request('hub.verify_token')
            print(token)

        if 'hub.challenge' in request:
            challenge = request('hub.challenge')
            print(challenge)
        
        if 'hub.mode' in request and 'hub.verify_token' in request:
            mode = request('hub.mode')
            token = request('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFICADO')

                challenge = request('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403
        
        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if  'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

                    return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404

        
    return render(request, 'api.html')

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='8888',debug=True)
    #port  =  int( os.environ.get ( "PORT" ,  5000 )) 
    #app.run(host = '0.0.0.0' ,  porta = port )