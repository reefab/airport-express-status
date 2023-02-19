import requests
import plistlib

AIRPORT_HOST = 'Ampli.local'

def get_status(host):
    data = plistlib.loads(requests.get(f'http://{host}:7000/info').content)
    return data['statusFlags']> 2000

print(get_status(AIRPORT_HOST))
