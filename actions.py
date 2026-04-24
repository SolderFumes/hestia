# This is where we parse a JSON file(?) With the following format:
# {
#   'https://homeassistant.local:8123/api/endpoint': {
#        'entity_id': 'light_switch',
#        data2..
#        },
#   url: data,
#   ...
# }
# So pretty much a dictionary where each key is a URL and each value is a dictionary containing the data to send!

# 1) Open the file
# 2) Read the data
# 3) Return the data!

# We can call this function as often as we want because it's just performing file I/O. We'll call this every 5 seconds or so.

import json

def get_actions(filename: str = 'actions.json'):
    with open(filename, 'r') as file:
        return json.load(file)

def actions_pretty(filename: str = 'actions.json'):
    '''
    Returns a List of tuples in which the first element is the type of the first entry in the JSON file filname and the second element is the entity_id.
    '''
    entity_type = ''
    entity_id = ''
    retlist = []
    data = get_actions()
    for key, value in data.items():
        entity_type = key.split('/')[1] # this should always be the type
        if entity_type == 'media_player':
            entity_type = 'Media Player'
        entity_id = value['entity_id']
        retlist.append((entity_type, entity_id))
    print('Prettified list:',retlist)
    return retlist



# We also want to be able to write the data to the file. We'll just take the dictionary as an argument and make someone else edit the dictionary. We supply a helper function to allow them to get the dictionary though, that way they don't have to do any file openining :) yay helpful
def write_data(data: dict, filename: str = 'actions.json'):
    with open(filename, 'w'):
        json.dumps(json, indent=4)


