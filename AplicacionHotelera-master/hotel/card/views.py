from django.shortcuts import render
from django.http import JsonResponse
from accesos.models import Usr
import requests 
import time
import hashlib
from base64 import b64encode

# Create your views here.
def index(request):
    # print(request.session['nombres'])
    print('card view')    
    print(request.user.username)    
    print('###################')
    print(type(request.user))
    return render(request, 'card/index.html', {"uid":request.session['customer']['username'], "email":request.session['customer']['email']})

def showCards(request):
    URL = "https://ccapi-stg.paymentez.com/v2/card/list"
    # location given here 
    uid = request.session['customer']['username']
    
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'uid':uid} 


    server_application_code = 'INNOVA-EC-SERVER'
    server_app_key = 'Y5FnbpWYtULtj1Muvw3cl8LJ7FVQfM'
    unix_timestamp = str(int(time.time()))
    #print('UNIX TIMESTAMP: %s' % unix_timestamp)
    uniq_token_string = server_app_key + unix_timestamp
    #print('UNIQ STRING: %s' % uniq_token_string)
    uniq_token_hash = hashlib.sha256(uniq_token_string.encode('utf-8')).hexdigest()
    #print('UNIQ HASH: %s' % uniq_token_hash)
    auth_token = b64encode(('%s;%s;%s' % (server_application_code,
    unix_timestamp, uniq_token_hash)).encode('UTF-8'))
    #print('AUTH TOKEN: %s' % auth_token.decode('UTF-8'))
    token = auth_token.decode('UTF-8')

    # sending get request and saving the response as response object 
    r = requests.get(url = URL, headers={'Auth-Token': token},params = PARAMS) 
    
    # extracting data in json format 
    data = r.json() 
    return JsonResponse(data)
    