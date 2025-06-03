import threading
from requests import get, post
from secrets import secrets
from cv import FaceRecognition, face_confidence

# start facial recognition while still being able to execute the rest of this program :) maybe make a main where we can use this python file for API calls and the cv.py for cv as we are doing here :) 
#
# <cv.py> ---[RUN FR]-----------------------
#                                          |----><main.py>
# <apicall.py> ---[CALL API BASED ON ARG]--- 
#
fr = FaceRecognition()
t1 = threading.Thread(target=fr.run_recognition)
t1.start()

api_key = secrets.get('homeassistant_api_key')
base_url = 'http://homeassistant.local:8123/api/'
headers = {
    'authorization': f'Bearer {api_key}',
    'content-type': 'application/json'
}
data = {'entity_id': 'light.lukafloodlight'}

light_is_on = False
while True:
    if ('Luka' in fr.get_face_names()):
        if not light_is_on:
            post(base_url + 'services/light/turn_on', headers=headers, json=data)
            print('turning light on..')
            light_is_on = True
    else: 
        if light_is_on:
            post(base_url + 'services/light/turn_off', headers=headers, json=data)
            print('turning light off..')
        light_is_on = False
    if not t1.is_alive():
        break




