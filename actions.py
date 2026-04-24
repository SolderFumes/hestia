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

import ast

def get_actions(filename: str = 'actions.hst'):
    with open(filename, 'r') as file:
        return ast.literal_eval(file.read()) 

def actions_pretty(filename: str = 'actions.json') -> list:
    '''
    Returns a List of tuples in which the first element is the type of the first entry in the JSON file filname and the second element is the entity_id.
    '''
    entity_type = ''
    entity_id = ''
    retlist = []
    data = get_actions()
    for action_tuple in data:
        for key, value in action_tuple[1].items():
            if key == 'entity_id':
                entity_id = value
                entity_type = action_tuple[0].split('/')[1] # This should always be the entity type
                retlist.append((entity_type, entity_id))
    print('prettified:', retlist)
    return retlist




def write_data(data: list, filename: str = 'actions.hst'):
    '''
    Writes string representation of actions list to filename provided
    '''
    with open(filename, 'w') as file:
        file.write(str(data))


