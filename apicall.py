import threading
from requests import get, post
from hestiasecrets import secrets
from cv import FaceRecognition, face_confidence

#
# <cv.py> ---[RUN FR]-----------------------
#                                          |----><main.py>
# <apicall.py> ---[CALL API BASED ON ARG]--- 
#

api_key = secrets.get('homeassistant_api_key')
base_url = 'http://homeassistant.local:8123/api/'
headers = {
    'authorization': f'Bearer {api_key}',
    'content-type': 'application/json'
}



def post_api(url, data):
    return post(base_url + url, headers=headers, json=data)
def get_api(url):
    return get(base_url + url, headers=headers)
