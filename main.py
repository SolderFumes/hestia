# The main file for running hestia (at the moment)
# Luka Schuller
# Created: Jun 2 2025
# i havent really decided on signiatures but who gaf LOL
from cv import FaceRecognition, face_confidence
import threading
import sys
from apicall import post_api

light_on_url = 'services/light/turn_on'
light_off_url = 'services/light/turn_off'

play_media_url = 'services/media_player/play_media'

# Start facial recognition in a thread
fr = FaceRecognition()
t1 = threading.Thread(target=fr.run_recognition)
t1.start()




light_data = {'entity_id': 'light.lukafloodlight'}
announce_data = {
    'entity_id': 'media_player.sonos_roam',
    'announce': 'true',
    'media_content_id': f'media-source://tts/cloud?message="Welcome, Luka. Now playing Sling by Clairo."' ,
    # maybe make a "preference" object and have the name and song name be like preference.name and preference.song_name
    'media_content_type': 'music'
}
song_data = announce_data.copy()
song_data['announce'] = 'false'
song_data['media_content_id'] = 'https://open.spotify.com/album/32ium7Cxb1Xwp2MLzH2459?si=o5UbpXJfRmqVs8gKCr5b4Q'


light_is_on = False
# Main loop
while True:
    if 'Luka' in fr.get_face_names():
        if not light_is_on:
            post_api(light_on_url, light_data)
            post_api(play_media_url, announce_data)
            post_api(play_media_url, song_data)
            light_is_on = True
    # if presence detector says nobody's home, turn everything off
    # since the presence detector is in homeassistant, it may be better to only check for presence every so often while the light is on, that way we don't spam the API too much.
    if not t1.is_alive():
        sys.exit()
