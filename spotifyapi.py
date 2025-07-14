from hestiasecrets import secrets
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_id = secrets['spotify_client_id']
client_secret = secrets['spotify_client_secret']

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get_song (string url --> tuple(song_name, artist_name)
# maybe get image preview as well
def get_song(song_url):
    # query spotify api
    # return song_name
    if 'track' in song_url:
        track = sp.track(song_url)
        return (track['name'], track['artists'][0]['name'])
    elif 'album' in song_url:
        album = sp.album(song_url)
        return (album['name'], album['artists'][0]['name'])
    elif 'playlist' in song_url:
        playlist = sp.playlist(song_url)
        return (playlist['name'], playlist['owner']['display_name'])

if __name__ == '__main__':
    print(get_song('https://open.spotify.com/playlist/6H5yldFpBfuIXRYJBYmqz9?si=rQO_xVUxQEa4sB8XellZEQ'))
