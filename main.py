# The main file for running hestia (at the moment)
# Luka Schuller
# Created: Jun 2 2025
from cv import FaceRecognition
import app
import threading
import sys
from time import sleep
from datetime import datetime
from apicall import post_api, get_api
import actions


shuffle = True

# Start facial recognition in a thread
fr = FaceRecognition()
t1 = threading.Thread(target=fr.run_recognition)
t1.start()

# Start Flask Webserver
t2 = threading.Thread(target=app.main)
t2.start()

presence = False
# Check the presence every 5 seconds
def presence_check():
    global presence
    while True:
        presence = True if get_api(get_presence_url).json().get('state') == 'on' else False
        sleep(1)

t3 = threading.Thread(target=presence_check)
t3.daemon = True
t3.start()

last_reg_time = None 
seconds_since_last_reg = lambda: (datetime.now() - last_reg_time).total_seconds()



shuffle_data = {
    'entity_id': 'media_player.sonos_roam',
    'shuffle': 'true'
}

room_is_on = False
user_name = None
# Main loop
while True:
    # get user if one is detected
    found_faces = fr.get_face_names()
    if len(found_faces) > 0 and not room_is_on:
        user_name = found_faces[0] # get first person to be detected
        if user_name == 'Unknown':
            continue

        ### ACTIVATE SMART HOME ###
        last_reg_time = datetime.now()
        print('turning on stuff...')
        ### PARSE DATA FILE ###
        actions_list = actions.get_actions()
        for url, data in actions_list:
            # if there's a media player, greet!
            if 'media_player' in url and not greeted:
                greeted = True
                post_api(url, {'entity_id': data['entity_id'], 'announce': True, 'media_content_type': 'music', 'media_content_id': f'media-source://tts/cloud?message="Welcome {user_name}!"'})
            post_api(url, data)
        if shuffle:
            post_api(shuffle_url, shuffle_data)
        room_is_on = True
# if presence detector says nobody's home, turn everything off
    if room_is_on and not presence and seconds_since_last_reg() > 10:
        # reset goobye and greet tracking
        greeted = False
        goodbyed = False
        print('stopping it all....')
        ### CALL RESET() FROM ACTIONS BASED ON ACTIONS FILE ###
        reset_list = actions.reset_actions('actions.hst')
        for url, data in reset_list
            if 'media_player' in url and not goodbyed:
                goodbyed = True
                post_api(url, {'entity_id': data['entity_id'], 'announce': True, 'media_content_type': 'music', 'media_content_id': f'media-source://tts/cloud?message="Goodbye {user_name}. Have a good one!"'})
            post_api(url, data)
        room_is_on = False

    # since the presence detector is in homeassistant, it may be better to only check for presence every so often while the light is on, that way we don't spam the API too much.
    if not t1.is_alive():
        sys.exit()
