import requests
from requests.auth import HTTPBasicAuth
import random

def create():
    base_url = 'https://api.plivo.com'
    req = requests.session()
    req.verify = False
    req.auth = HTTPBasicAuth('MAODUZYTQ0Y2FMYJBLOW', 'ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0')
    return base_url, req

def get_two_numbers():
    url, req = create()
    number_url =  url + '/v1/Account/%s/Number/' % req.auth.username
    response = req.get(number_url)
    if response.ok:
        num1, num2 = random.choices(response.json()['objects'], k=2)
        while num2 == num1:
            num1, num2 = random.choices(response.json()['objects'], k=2)
         
    return num1['number'], num2['number']

def message(source, destination, msg, callback_url):
    url, req = create()
    msg_url =  url + '/v1/Account/%s/Message/' % req.auth.username
    data = {
        'src': source,
        'dst': destination,
        'text': msg,
        'trackable': True,
        'url': callback_url
    }
    response = req.post(msg_url, json=data)
    if response.ok:
        #print (response.json())
        print ('message sent successfully\n  '
                'check status using this url : %s' % callback_url)
        return callback_url, response.json()['message_uuid'][0]

def create_end_point():
    url, req = create()
    endpoint_url = url + '/v1/Account/%s/Endpoint/' % req.auth.username
    data = {
        'username': req.auth.username,
        'password': req.auth.password,
        'alias': 'subhan'
    }
    response = req.post(endpoint_url, json=data)
    if response.ok:
        return response.json()['endpoint_id']

def get_call_back_url():
    end_point = create_end_point()
    base_url, req = create()
    url = base_url + '/v1/Account/%s/Endpoint/%s' % (req.auth.username, end_point)
    response = req.get(url)
    if response.ok:
        return base_url + response.json()['application'] 

def check_sms_status(url, mesg_id):
    base_url, req = create()
    data = {
        'MessageUUID': mesg_id
    }
    response = req.post(url, json=data)
    if response.ok:
        pass 

def get_msg_details(msg_id):
    url, req = create()
    url = url + '/v1/Account/%s/Message/%s' % (req.auth.username, msg_id)
    response = req.get(url)
    if response.ok:
        print(response.json()) 

s, d = get_two_numbers()
url, mesg_id = message(s,d, 'second text', get_call_back_url())
#check_sms_status(url, mesg_id)
get_msg_details(mesg_id)
