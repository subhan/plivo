import random

import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from functools import lru_cache


@lru_cache(maxsize=2)
def create_req_url():
    base_url = 'https://api.plivo.com'
    req = requests.session()
    req.verify = False
    req.auth = HTTPBasicAuth('MAODUZYTQ0Y2FMYJBLOW', 'ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0')
    return base_url, req


def get_two_numbers():
    uri, req = create_req_url()
    number_url = uri + '/v1/Account/%s/Number/' % req.auth.username
    response = req.get(number_url)
    if response.ok:
        num1, num2 = random.choices(response.json()['objects'], k=2)
        while num2 == num1:
            num1, num2 = random.choices(response.json()['objects'], k=2)
        return num1['number'], num2['number']
    raise Exception('Unable to get mobile numbers')


def message(source, destination, msg, callback_url):
    uri, req = create_req_url()
    msg_url = uri + '/v1/Account/%s/Message/' % req.auth.username
    data = {
        'src': source,
        'dst': destination,
        'text': msg,
        'trackable': True,
        'url': callback_url
    }
    response = req.post(msg_url, json=data)
    if response.ok:
        print('message sent successfully\n  '
              'check status using this url : %s' % callback_url)
        return callback_url, response.json()['message_uuid'][0]
    raise Exception('Unable to sent message')

def create_end_point():
    uri, req = create_req_url()
    endpoint_url = uri + '/v1/Account/%s/Endpoint/' % req.auth.username
    data = {
        'username': req.auth.username,
        'password': req.auth.password,
        'alias': 'subhan'
    }
    response = req.post(endpoint_url, json=data)
    if response.ok:
        return response.json()['endpoint_id']

    raise Exception('Unable to create end point')


def get_call_back_url():
    end_point = create_end_point()
    base_url, req = create_req_url()
    uri = base_url + '/v1/Account/%s/Endpoint/%s' % (req.auth.username, end_point)
    response = req.get(uri)
    if response.ok:
        return base_url + response.json()['resource_uri']
    raise Exception('Unable to get call back url')


def check_sms_status(call_back_url, mesg_id):
    _, req = create_req_url()
    data = {
        'MessageUUID': mesg_id
    }
    response = req.post(call_back_url, json=data)
    if response.ok:
        print(response.json())
    raise Exception('Unable to check sent message status')


def get_msg_details(mesg_id):
    url, req = create_req_url()
    url = url + '/v1/Account/%s/Message/%s' % (req.auth.username, mesg_id)
    response = req.get(url)
    if response.ok:
        print(response.json())


def get_pricing_details(country='US'):
    url, req = create_req_url()
    url = url + '/v1/Account/{1}/Pricing/?country_iso={2}'.format(
        req.auth.username, country)
    response = req.get(url)
    if response.ok:
        print(response.json())


def get_account_details():
    url, req = create_req_url()
    url = url + '/v1/Account/%s/' % req.auth.username
    response = req.get(url)
    if response.ok:
        print(response.json())


if __name__ == '__main__':
    get_account_details() 
    SRC, DST = get_two_numbers()
    _, MSG_ID = message(SRC, DST, 'fifth message', get_call_back_url())
    #check_sms_status(url, msg_id)
    get_msg_details(MSG_ID)
    get_pricing_details('IN')
