# The main file for running hestia (at the moment)
# Luka Schuller
# Created: Jun 2 2025
# i havent really decided on signiatures but who gaf LOL
from cv import FaceRecognition, face_confidence
from db import get_user
from spotifyapi import get_song
import app
import threading
import sys
import time
from datetime import datetime
from apicall import post_api, get_api
from reset import reset_all

get_presence_url = 'states/binary_sensor.human_presence_detector'
light_on_url = 'services/light/turn_on'
light_off_url = 'services/light/turn_off'
plug_on_url = 'services/switch/turn_on'
plug_off_url = 'services/switch/turn_off'
play_media_url = 'services/media_player/play_media'
shuffle_url = 'services/media_player/shuffle_set'

# set this in the DB later (haha not now hashtag restful queen)
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
        time.sleep(1)

t3 = threading.Thread(target=presence_check)
t3.daemon = True
t3.start()

last_reg_time = None 
seconds_since_last_reg = lambda: (datetime.now() - last_reg_time).total_seconds()



announce_data = {
    'entity_id': 'media_player.sonos_roam',
    'announce': 'true',
    'media_content_id': f'media-source://tts/cloud?message="Error. Announce Data has not been modified."' ,
    'media_content_type': 'music'
}
shuffle_data = {
    'entity_id': 'media_player.sonos_roam',
    'shuffle': 'true'
}
goodbye_data = announce_data.copy()
song_data = announce_data.copy()
song_data['announce'] = 'false'
song_data['media_content_id'] = 'https://open.spotify.com/album/32ium7Cxb1Xwp2MLzH2459?si=o5UbpXJfRmqVs8gKCr5b4Q'


room_is_on = False
user_name = None
# Main loop
while True:
    # get user if one is detected
    if fr.get_face_names() != [] and not room_is_on:
        user_name = fr.get_face_names()[0] # get first person to be detected
        user = get_user(user_name) # db object

        ### SET DATA ###
        r, g, b = user.light_color.split(',')
        announce_data['media_content_id'] = f'media-source://tts/cloud?message="Welcome, {user.name}. Now playing {user.song_name} by {user.song_artist}."'
        print('announce:',announce_data)
        song_data['media_content_id'] = user.song_url
        light_data = {'entity_id': 'light.big_lamp', 'rgb_color': [r,g,b]}
        plug1_data = {'entity_id': 'switch.under_desk_outlet_switch'} 
        plug2_data = {'entity_id': 'switch.under_desk_outlet_switch_2'}
        goodbye_data['media_content_id'] = f'media-source://tts/cloud?message="Goodbye, {user.name}! Have a good one!"'
    
        ### ACTIVATE SMART HOME ###
        last_reg_time = datetime.now()
        print('turning on stuff...')
        post_api(play_media_url, announce_data)
        post_api(light_on_url, light_data)
        post_api(play_media_url, song_data)
        post_api(plug_on_url, plug1_data)
        post_api(plug_on_url, plug2_data)
        if shuffle:
            print('call me cupid cause im shuffling')
            post_api(shuffle_url, shuffle_data)
        room_is_on = True
# if presence detector says nobody's home, turn everything off
    if room_is_on and not presence and seconds_since_last_reg() > 10:
        print('stopping it all....')
        post_api(play_media_url, goodbye_data)
        reset_all()
        room_is_on = False

    # since the presence detector is in homeassistant, it may be better to only check for presence every so often while the light is on, that way we don't spam the API too much.
    if not t1.is_alive():
        sys.exit()
