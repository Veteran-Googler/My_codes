import requests
from chess import pgn
import time
import io
import csv
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
headers={"User-Agent":f"GameStatisticsFetcher/1.0 (Contact: {'Xx_Queen-Seeker_xX'})"}
year=2024
month=11
users_file="players_lists_nov"

def get_opening_category(eco_code):
    # 1. SPECIALIST DEFENSES (Black Responses to e4)
    if "B20" <= eco_code <= "B99": return "Sicilian Defense"      # The biggest chunk of theory
    if "C00" <= eco_code <= "C19": return "French Defense"
    if "B10" <= eco_code <= "B19": return "Caro-Kann"
    if "B06" <= eco_code <= "B09": return "Pirc / Modern"
    if "B00" <= eco_code <= "B05": return "Alekhine / Scandi"     # Hyper-modern e4 defenses

    # 2. OPEN GAMES (1.e4 e5)
    if "C60" <= eco_code <= "C99": return "Ruy Lopez (Spanish)"   # Distinct enough to be its own bar
    if "C20" <= eco_code <= "C59": return "Italian / Scotch"      # All other e4 e5 games

    # 3. CLOSED GAMES (1.d4 d5)
    if "D06" <= eco_code <= "D69": return "Queen's Gambit"        # The classical QGD/Slav complex
    if "D00" <= eco_code <= "D05": return "London / System d4"    # The "Boring" d4 systems (London, Colle)

    # 4. INDIAN SYSTEMS (1.d4 Nf6)
    if "E60" <= eco_code <= "E99": return "King's Indian / Grunfeld" # Kingside Fianchetto systems
    if "E00" <= eco_code <= "E59": return "Nimzo / Queen's Indian"   # Light-square control systems
    if "A80" <= eco_code <= "A99": return "Dutch Defense"            # Assymmetric f5 defense
    if "A50" <= eco_code <= "A79": return "Benoni / Benko"           # Chaos d4 systems

    # 5. FLANK & IRREGULAR
    if "A10" <= eco_code <= "A39": return "English Opening"       # 1. c4
    if "A00" <= eco_code <= "A09": return "Reti / Irregular"      # 1. Nf3, 1. b3, 1. f4 (Bird)
    if "D70" <= eco_code <= "D99": return "Grunfeld Defense"      # The missing link!
    if "A40" <= eco_code <= "A49": return "Queen's Pawn / Tromp"  # Captures Trompowsky & London variations
    return "Other" # Safety net
#base Function to get games
def get_games(username, target_year, target_month):
    time.sleep(0.5)#overcome the api limit. Note:i should consider learning asyncio for better performance
    url=f"https://api.chess.com/pub/player/{username}/games/{target_year}/{target_month}"
    try:
        response=requests.get(url, headers=headers)
        if response.status_code!=200:
           print(f"Failed to fetch archives for {username}")
           return []
        return response.json().get("games", [])
    except Exception as e:
        print(f"[!] Connection Skipped for {username}: {e}")
        return []
#function to get the pgns from the games
def get_pgn(games):
    pgns=[]
    for game in games:
            if game.get("pgn"):
                pgns.append(game.get("pgn"))
            else:
                continue
    return pgns
#function to get wanted info from the pgn aka:elo and oppening
def get_the_elo_and_the_oppening(pgn_code):
    object_game=pgn.read_game(io.StringIO(pgn_code))
    if object_game is None:
        return [0,0]
    dict_game=object_game.headers
    eco_code=dict_game.get('ECO', "?")
    oppening=get_opening_category(eco_code)
    White_elo=dict_game.get('WhiteElo', '?')
    Black_elo=dict_game.get('BlackElo', '?')
    if White_elo.isdigit() and Black_elo.isdigit():
        Average_elo=(int(White_elo)+int(Black_elo))/2
        return [Average_elo,oppening]
    else:
        return [0,oppening]
oppenings_table={}
#main program to get the statistics
with open(users_file, "r") as file:
    for line in file:
        user=line.strip()
        games=get_games(user,year,month)
        pgns=get_pgn(games)
        for pgn_code in pgns:
            elo_and_oppening=get_the_elo_and_the_oppening(pgn_code)
            oppening=elo_and_oppening[1]
            elo=elo_and_oppening[0]
            category=(elo//200)*200
            if category in oppenings_table.keys():
                category_dict=oppenings_table.get(category)
                if oppening in category_dict.keys():
                    category_dict[oppening]+=1
                else:
                    category_dict[oppening]=1
            else:
                oppenings_table[category]={oppening:1}
        csv_filename = "Oppenings_stats.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
           writer = csv.writer(file)
           writer.writerow(["Elo_Range", "Opening_Name", "Games_Count"])
           for elo_category, opening_data in oppenings_table.items():
               for opening_name, count in opening_data.items():
                   writer.writerow([elo_category, opening_name, count])

print("Exporting to CSV...")
csv_filename = "Oppenings_stats.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Elo_Range", "Opening_Name", "Games_Count"])
    for elo_category, opening_data in oppenings_table.items():
        for opening_name, count in opening_data.items():
            writer.writerow([elo_category, opening_name, count])
print(f"Success. Data saved to {csv_filename}")

            

    
            
