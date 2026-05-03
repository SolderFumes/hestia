from apicall import post_api

def reset_all():
    post_api('services/light/turn_off', {'entity_id': 'light.big_lamp'})
    post_api('services/media_player/media_pause', {'entity_id': 'media_player.sonos_roam'})
    post_api('services/switch/turn_off', {'entity_id': 'switch.under_desk_outlet_switch'})
    post_api('services/switch/turn_off', {'entity_id': 'switch.under_desk_outlet_switch_2'})
    post_api('services/media_player/play_media', {'entity_id': 'media_player.bedroom'} + goodbye_data)
    goodbye_data['media_content_id'] = f'media-source://tts/cloud?message="Goodbye, {user.name}! Have a good one!"'


if __name__ == '__main__':
    reset_all()
