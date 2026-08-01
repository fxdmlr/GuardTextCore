import requests
import json

url = 'https://guardts.ir/api/pastes/'

def create_paste(address, msg):
    r = requests.post(url, data={
        "content": str(msg),
        "customSlug": str(address),
        "expiresIn" : "1"
    })
    return r

def read_paste(address):
    r = requests.get(url + address).text
    d = json.loads(r)
    return d["content"]

