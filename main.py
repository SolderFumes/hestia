# The main file for running hestia (at the moment)
# Luka Schuller
# Created: Jun 2 2025
# i havent really decided on signiatures but who gaf LOL
from cv import FaceRecognizer, face_confidence
from apicall import post_api

light_on_url = 'services/light/turn_on'
light_off_url = 'services/light/turn_off'

# Start facial recognition in a thread
fr = FaceRecognition()
t1 = threading.Thread(target=fr.run_recognition)
t1.start()




data = {'entity_id': 'light.lukafloodlight'}

light_is_on = False
# Main loop
while True:
    if 'Luka' in fr.get_face_names():
        if not light_is_on:
            post_api(light_on_url, data)
            light_is_on = True
    # if presence detector says nobody's home, turn everything off
    # since the presence detector is in homeassistant, it may be better to only check for presence every so often while the light is on, that way we don't spam the API too much.
