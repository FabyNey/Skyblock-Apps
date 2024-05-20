import requests
from pprint import pprint
from datetime import datetime
import json

# Function to make API calls
def get_info(url):
    r = requests.get(url)
    return r.json()

# Function to get bazaar information
def get_bazaar_info():
    return get_info("https://api.hypixel.net/v2/skyblock/bazaar")

# Function to get player information
def get_player_info(profile_id):
    return get_info(f"https://api.hypixel.net/v2/skyblock/profile?key={API_KEY}&profile={profile_id}")

# Function to calculate forge process completion time
def calculate_forge_completion(start_time):
    return datetime.fromtimestamp((start_time / 1000) + 21600).strftime('%Y-%m-%d %H:%M:%S')

API_FILE = open("hypixel api/API_KEY.json", "r")
API_KEY = json.loads(API_FILE.read())["API_KEY"]
my_profile_id = "f7e8c06d-6237-44be-9f76-0813f84cbdf1" 

while True:
    user_input = int(input("Enter 1 to get melon profits or 2 to check forge status: "))
    
    if user_input == 1:
        bazaar_data = get_bazaar_info()
        print(datetime.now().strftime("%Y-%m-%d %H:%M"))
        enchanted_melon_block_sell_price = bazaar_data["products"]["ENCHANTED_MELON_BLOCK"]["quick_status"]["sellPrice"]
        player_data = get_player_info(my_profile_id)
        coins = int(player_data["profile"]["members"]["1a8b0e3d301d4f77916ec0d94d0eb16f"]["currencies"]["coin_purse"])
        profit = 51200 - enchanted_melon_block_sell_price
        melons_to_buy = int(coins / enchanted_melon_block_sell_price)
        coin_profit = int(melons_to_buy * profit)
        coins_to_spend = int(melons_to_buy * enchanted_melon_block_sell_price)
        if profit > 0:
            print(f"For every melon bought, there is a profit of {profit} coins.")
            print(f"You can buy {melons_to_buy} melons to make a profit of {coin_profit}, spending {coins_to_spend / 1000000} million coins.")
    elif user_input == 2:
        player_data = get_player_info(my_profile_id)
        for i in range(1, 6):
            forge_data = player_data["profile"]["members"]["1a8b0e3d301d4f77916ec0d94d0eb16f"]["forge"]["forge_processes"]["forge_1"][str(i)]
            notified = forge_data["notified"]
            start_time = forge_data["startTime"]
            if not notified:
                completion_time = calculate_forge_completion(start_time)
                print(f"Forge {i} is still going on. If it was enchanted mithril, it will finish at {completion_time}")
            else:
                print(f"Forge {i} has finished.")
    else:
        print("Enter a valid input (1 or 2).")
