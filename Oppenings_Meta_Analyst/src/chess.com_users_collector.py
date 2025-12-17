import requests
from chess import pgn
import time
import io
seed=["giga_dummy", "The_game_of_art", "OGKrustytheKlown","NicolasL201", "hhalf", "3x6x9", "Qwertyz24", "okletsplay1234", "will669", "LiamGH", "Caevita", "C_Lee", "Rjames507", "jsinger", "thebishopswinger", "sergioib"]
headers={"User-Agent":f"GameStatisticsFetcher/1.0 (Contact: {'Xx_Queen-Seeker_xX'})"}
month=11
year=2025
i=0
#base function to get games as dictionnaries
def get_games(username, target_year, target_month):
    time.sleep(0.5)
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
#Function to get the pgns played by the users in the wanted month, based on the base function
def get_pgns(users, year, month):
    global i
    pgns=[]
    for user in users:
        i+=1
        games= get_games(user, year, month)
        for game in games:
            if game.get("pgn"):
                pgns.append(game.get("pgn")) 
            else:
                continue
        print(f"{i}.returning pgns for {user} ")
    return pgns
#function to get the player and their opponents from the pgn
def get_the_players(pgn_code):
    object_game=pgn.read_game(io.StringIO(pgn_code))
    if object_game is None:
        return []
    dict_game=object_game.headers
    players=[dict_game.get('White', '?'), dict_game.get('Black', '?')]
    return players
#Function that use a spider algorithm to collect several usernames
def spider_players_search(seed, year, month,depth,max):
    players= set(seed)#initialisation of the first players
    with open("players_lists_nov", "a", encoding="utf-8") as file:
        for player in players:
            file.write('\n'+ player)
    new_players=list(players) #initialisation of the new players list
    for _ in range(depth):
        pgns=get_pgns(new_players, year, month)
        new_players=[]#updating the new players list
        if len(players)>=max:
            break
        for pgn_code in pgns:
            opponents=get_the_players(pgn_code)#get the players playing in each pgn code
            for player in opponents:
                if player not in players and player != "?" and player is not None:#verifying if the player don't exist in the players set
                    players.add(player)
                    new_players.append(player)#collecting the new players
                    with open("players_lists_nov", "a", encoding="utf-8") as file:
                        file.write('\n'+player)
            if len(players)>=max:
                break
    print(f"players are written in the players_list file")
    return players


final_list=spider_players_search(seed,2025,12,3, 5000)



