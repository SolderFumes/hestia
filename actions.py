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
    data = get_actions(filename)
    for action_tuple in data:
        for key, value in action_tuple[1].items():
            if key == 'entity_id':
                entity_id = value
                entity_type = action_tuple[0].split('/')[1] # This should always be the entity type
                retlist.append((entity_type, entity_id))
    return retlist

def count_entity_occurances(filename: str) -> dict:
    '''
    Goes through a hestia-formatted list of actions and returns a dict
    with the following format:
    { entity_id: count }.
    '''
    data = []
    with open(filename, 'r') as file:
        data = ast.literal_eval(file.read())
    retdict = {'': float('-inf')}
    for _, data_dict in data:
        for key in data_dict.keys():
            if key == 'entity_id':
                entity_id = data_dict['entity_id']
                if entity_id in retdict.keys():
                    retdict[entity_id] += 1
                else:
                    retdict[entity_id] = 1
    return retdict

def add_actions(data: list, filename: str = 'actions.hst') -> None:
    '''
    Turns an input list of new actions from app.py into hestia-formatted text
    and appends it to actions file.
    '''
    original_occurance_dict = count_entity_occurances(filename)
    occurance_count = {'': float('-inf')} # empty string is nothing but its always tere
    print('original occurance count:', original_occurance_dict)
    append_list = []
    for url, entity_id in data:
        if entity_id in original_occurance_dict.keys():
            print(f'Entity {entity_id} is already in our config. It appeared {original_occurance_dict[entity_id]} times.')
            # ^^^ if the entity id is already in our config
            if entity_id in occurance_count.keys():
                print(f'Entity {entity_id} is already in our counting dict. It\'s value is {occurance_count[entity_id]}.')
            # ^^^ if we have already started counting this entity. We're going to add
            # 1 to the counter either way, but python requires us to check if the
            # key already exists.
                occurance_count[entity_id] += 1
            else:
                occurance_count[entity_id] = 1
            if original_occurance_dict[entity_id] < occurance_count[entity_id]:
                # its a new entity occurance, add it! Hand it to handle_new_entity_occurance to see if its a duplicate and add the custom functionality
                #TODO: handle_new_entity_occurance(entity_id)
                printf('Entity {entity_id} has more occurances in the form than in our stored version! We are appending it to append_list.')
                append_list.append((url, convert_to_default_data((url, entity_id))))
        else:
            # if its a new entity create default data for it
            print('Entity {entity_id} exists in the form but not in the stored file! Adding it to append_list.')
            append_list.append((url, convert_to_default_data((url, entity_id))))
    current_list = get_actions(filename)
    write_data(current_list + append_list, filename)
    print(f'Actions have been written! List from form: {current_list}\nAppend list: {append_list}\nResult list: {get_actions(filename)}')

def convert_to_default_data(entity: tuple) -> dict:
    url = entity[0]
    entity_id = entity[1]
    data = {'entity_id': entity_id}
    match entity_id.split('.')[0]:
        case 'light':
            #There's nothing that goes in a light's data other than it's entity_id by default.
            pass
        case 'switch':
            # see comment above
            pass
        case 'media_player':
            data['announce'] = True
            data['media_content_id'] = 'media-source://tts/cloud?message=\"This is the default media player action. Please change it!\"'
            data['media_content_type'] = 'music'
    return data


def write_data(data: list, filename: str = 'actions.hst'):
    '''
    Writes string representation of actions list to filename provided
    '''
    with open(filename, 'w') as file:
        file.write(str(data))


