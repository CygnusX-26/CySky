import requests
import json
from pprint import pprint
from username_to_uuid import UsernameToUUID


def getInfo(call):
    r = requests.get(call)
    return r.json()


name = "labhs"
API_KEY = "7b547f0d-efc7-4e9e-9fdd-7e0f5b68f9ca"
name_link = getInfo(
    f"https://api.hypixel.net/player?key={API_KEY}&name={name}")
converter = UsernameToUUID("labhs")
uuid = converter.get_uuid()
#skyblock_id = list(name_link['player']['stats']['SkyBlock']['profiles'].keys())[0]
#profile = getInfo(f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={uuid}")
#bazaar_data = getInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}')
#item_data = getInfo(f'https://api.hypixel.net/resources/skyblock/items?key={API_KEY}')
#auction_data = getInfo(f'https://api.hypixel.net/skyblock/auction?key={API_KEY}&player={uuid}')
pprint()
