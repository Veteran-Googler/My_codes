import requests
import pandas as pd
import matplotlib.pyplot as plt
months=1 #number of months to fetch
user="Xx_Queen-Seeker_xX"
headers={"User-Agent":f"GameStatisticsFetcher/1.0 (Contact: {user})"}
url=f"https://api.chess.com/pub/player/{user}/games/archives"
#get lists of archives
response=requests.get(url,headers=headers)
with open("chess_games.txt","w") as file:
    file.write(response.text)
print("Chess game archives fetched and saved to chess_games.txt")
archive_list=response.json().get("archives",[])
archive_list=archive_list[-months:]  #get last  wanted months
with open("chess_games_archives.txt", "w") as file:
    pass # Clear the file before appending
for archive_url in archive_list:
    archive_response=requests.get(archive_url,headers=headers)
    with open("chess_games_archives.txt","a") as file:
        file.write("\n"+archive_response.text)
    print(f"Fetched and appended games from archive: {archive_url}")
print("All chess game archives fetched and saved to chess_games_archives.txt")
# slicing the data to extract the individual games pgn (from 'pgn' to ,)
games_data=[]
with open("chess_games_archives.txt","r") as file:
    data=file.read()
pgns=data.split('"pgn":"')[1:]
for pgn in pgns:
    game_pgn=pgn.split('","')[0]
    games_data.append(game_pgn.replace('\\n','\n').replace('\\"','"'))

print(games_data[0])  # Print the first game's PGN as a sample
#build a csv file with columns:Color,Result,Castle:
with open("chess_games_analysis.csv","w") as file:
    file.write("Color,Result,Castle\n")
    for game_pgn in games_data:
        color= None
        result= None
        for line in game_pgn.split('\n'):   
            if user in line:
                if 'White' in line:
                    color='White'
                elif 'Black' in line:
                    color='Black'
                
            if 'Result' in line:
                if '/' in line:
                    result='Draw'
                elif '1-0' in line and color=='White':
                    result='Win'
                elif '0-1' in line and color=='Black':
                    result='Win'
                else:
                    result='Loss'
        if color is None:
            continue  #skip if user not found
        castle='-'
        moves=game_pgn.split('{')[0:-1]
        if color=='White':
            start=0
        else:
            start=1
        for move in moves[start::2]:
            if 'O-O-O'in move:
                castle='Long'
                break
            elif 'O-O'in move:
                castle='Short'
                break
        file.write(f"{color},{result},{castle}\n")
print("Chess games analysis saved to chess_games_analysis.csv")
print(pd.read_csv("chess_games_analysis.csv"))
#Make a list of each column
data_df=pd.read_csv("chess_games_analysis.csv")
colors=data_df['Color'].tolist()
results=data_df['Result'].tolist()
castles=data_df['Castle'].tolist()
#print the count of wins,losses,draws
win_count=results.count('Win')
loss_count=results.count('Loss')
draw_count=results.count('Draw')
print(f"Wins: {win_count}, Losses: {loss_count}, Draws: {draw_count}")
#plot a pie chart of results
labels=['Wins','Losses','Draws']
sizes=[win_count,loss_count,draw_count]
plt.figure(figsize=(8,8))
plt.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=140)
plt.title(f"Game Results for {user}")
plt.show()
# print the count of wins,losses,draws with White and Black
white_wins=sum(1 for i in range(len(results)) if results[i]=='Win' and colors[i]=='White')
black_wins=sum(1 for i in range(len(results)) if results[i]=='Win' and colors[i]=='Black')
white_losses=sum(1 for i in range(len(results)) if results[i]=='Loss' and colors[i]=='White')
black_losses=sum(1 for i in range(len(results)) if results[i]=='Loss' and colors[i]=='Black')
white_draws=sum(1 for i in range(len(results)) if results[i]=='Draw' and colors[i]=='White')
black_draws=sum(1 for i in range(len(results)) if results[i]=='Draw' and colors[i]=='Black')
print(f"White Wins: {white_wins}, White Losses: {white_losses}, White Draws: {white_draws}")
print(f"Black Wins: {black_wins}, Black Losses: {black_losses}, Black Draws: {black_draws}")
#plot a pie chart of results by color
labels=['White Wins','White Losses','White Draws','Black Wins','Black Losses','Black Draws']
sizes=[white_wins,white_losses,white_draws,black_wins,black_losses,black_draws]
plt.figure(figsize=(8,8))
plt.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=140)
plt.title(f"Game Results by Color for {user}")
plt.show()
# print the count of wins, losses, draws with short and long castles and no castles
short_castle_wins=sum(1 for i in range(len(results)) if results[i]=='Win' and castles[i]=='Short')
long_castle_wins=sum(1 for i in range(len(results)) if results[i]=='Win' and castles[i]=='Long')
no_castle_wins=sum(1 for i in range(len(results)) if results[i]=='Win' and castles[i]=='-')
short_castle_losses=sum(1 for i in range(len(results)) if results[i]=='Loss' and castles[i]=='Short')
long_castle_losses=sum(1 for i in range(len(results)) if results[i]=='Loss' and castles[i]=='Long')
no_castle_losses=sum(1 for i in range(len(results)) if results[i]=='Loss' and castles[i]=='-')
short_castle_draws=sum(1 for i in range(len(results)) if results[i]=='Draw' and castles[i]=='Short')
long_castle_draws=sum(1 for i in range(len(results)) if results[i]=='Draw' and castles[i]=='Long')
no_castle_draws=sum(1 for i in range(len(results)) if results[i]=='Draw' and castles[i]=='-')
print(f"Short Castle Wins: {short_castle_wins}, Short Castle Losses: {short_castle_losses}, Short Castle Draws: {short_castle_draws}")
print(f"Long Castle Wins: {long_castle_wins}, Long Castle Losses: {long_castle_losses}, Long Castle Draws: {long_castle_draws}")
print(f"No Castle Wins: {no_castle_wins}, No Castle Losses: {no_castle_losses}, No Castle Draws: {no_castle_draws}")
#plot a pie chart of results by castle type
labels=['Short Castle Wins','Short Castle Losses','Short Castle Draws',
        'Long Castle Wins','Long Castle Losses','Long Castle Draws',
        'No Castle Wins','No Castle Losses','No Castle Draws']
sizes=[short_castle_wins,short_castle_losses,short_castle_draws,
       long_castle_wins,long_castle_losses,long_castle_draws,
         no_castle_wins,no_castle_losses,no_castle_draws]
plt.figure(figsize=(10,10))
plt.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=140)
plt.title(f"Game Results by Castle Type for {user}")
plt.show()

            

    







