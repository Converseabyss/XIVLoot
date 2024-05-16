import json
import os

def get_data_file_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'data.json')

def load_data():
    data_file = get_data_file_path()
    with open(data_file, 'r') as file:
        return json.load(file)

def save_data(data):
    data_file = get_data_file_path()
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

def add_boss(data, boss_name):
    if boss_name not in data['bosses']:
        data['bosses'].append(boss_name)
        for player in data['players']:
            player['locked'][boss_name] = False
        save_data(data)

def lock_player(data, player_name, boss_name):
    for player in data['players']:
        if player['name'] == player_name:
            player['locked'][boss_name] = True
    save_data(data)

def unlock_player(data, player_name, boss_name):
    for player in data['players']:
        if player['name'] == player_name:
            player['locked'][boss_name] = False
    save_data(data)
    
def remove_boss(data, boss_name):
    if boss_name in data['bosses']:
        data['bosses'].remove(boss_name)
        for player in data['players']:
            if boss_name in player['locked']:
                del player['locked'][boss_name]
        save_data(data)