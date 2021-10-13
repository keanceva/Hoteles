import time
import hashlib
from base64 import b64encode

class CardToken(object):
    def __init__(self, cardToken=None):
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
        self.cardToken = auth_token.decode('UTF-8')