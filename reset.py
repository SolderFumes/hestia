from apicall import post_api

def reset_all():
    post_api('services/light/turn_off', {'entity_id': 'light.lukafloodlight'})
    post_api('services/media_player/media_pause', {'entity_id': 'media_player.sonos_roam'})


if __name__ == '__main__':
    reset_all()
