from apicall import post_api

def reset_all():
    post_api('services/light/turn_off', {'entity_id': 'light.big_lamp'})
    post_api('services/media_player/media_pause', {'entity_id': 'media_player.sonos_roam'})
    post_api('services/switch/turn_off', {'entity_id': 'switch.under_desk_outlet_switch'})
    post_api('services/switch/turn_off', {'entity_id': 'switch.under_desk_outlet_switch_2'})


if __name__ == '__main__':
    reset_all()
