from chess import pgn
import requests
import pandas as pd
import json
import io
import matplotlib.pyplot as plt
months=1#number of months to fetch
user="Xx_Queen-Seeker_xX"
headers={"User-Agent":f"GameStatisticsFetcher/1.0 (Contact: {user})"}
url=f"https://api.chess.com/pub/player/{user}/games/archives"
pgn_list=[]
#get lists of archives
response=requests.get(url,headers=headers)

print("Chess game archives fetched and saved to chess_games.txt")
archive_list=response.json().get("archives",[])
archive_list=archive_list[-months:]  #get last  wanted months
with open("chess_games_archives.txt", "w") as file:
    pass # Clear the file before appending
for archive_url in archive_list:
    print(f"Fetching games from archive: {archive_url}")
    response_archive=requests.get(archive_url,headers=headers)
    data=response_archive.json()
    games=data.get("games",[])
    with open("chess_games_archives.txt","a") as file:
        for game in games:
            pgn_text=game.get("pgn","")
            pgn_list.append(pgn_text)
            file.write("\n"+pgn_text)
    print(f"Fetched and appended games from archive: {archive_url}")
print("All pgn game archives fetched and saved to chess_games_archives.txt")
# create a dataframe of oppenings, number of wins and losses
oppenings=[]
results=[]
for pgn_text in pgn_list:
    game=pgn.read_game(io.StringIO(pgn_text))
    headers=game.headers
    result=headers.get("Result","*")
    White=headers.get("White","Unknown Player")
    if White.lower()==user.lower():
        color="White"
        if result=="1-0":
            outcome="Win"
        elif result=="0-1":
            outcome="Loss"
        else:
            outcome="Draw"
    elif headers.get("Black","Unknown Player").lower()==user.lower():
        color="Black"
        if result=="1-0":
            outcome="Loss"
        elif result=="0-1":
            outcome="Win"
        else:
            outcome="Draw"
    opening=headers.get("ECOUrl","Unknown Opening")
    opening=opening.split("/")[-1].split("-")[0] if opening!="Unknown Opening" else opening
    opening=opening+color #The fix to differenciate between if the user played white or black
    oppenings.append(opening)
    results.append(outcome)
# create a dataframe
df=pd.DataFrame({"Opening":oppenings,"Result":results})
print(df)
with open("chess_opening_analysis.json","w") as file:
    summary=df.groupby(["Opening","Result"]).size().unstack(fill_value=0).to_json()
    file.write(summary)
# analyze the dataframe to get number of wins and losses per opening
data={}
for opening in df["Opening"].unique():
    win_count=df[(df["Opening"]==opening) & (df["Result"]=="Win")].shape[0]
    loss_count=df[(df["Opening"]==opening) & (df["Result"]=="Loss")].shape[0]
    draw_count=df[(df["Opening"]==opening) & (df["Result"]=="Draw")].shape[0]
    print(f"Opening: {opening}, Wins: {win_count}, Losses: {loss_count}, Draws: {draw_count}")
    data[opening]=[win_count, loss_count, draw_count]
# plot the data as bar chart with  3 colors for wins, losses and draws one on top of the other for each opening
openings=list(data.keys())
win_counts=[data[opening][0] for opening in openings]
loss_counts=[data[opening][1] for opening in openings]
draw_counts=[data[opening][2] for opening in openings]
x=list(range(len(openings)))
plt.bar(x, win_counts, color='g', label='Wins')
plt.bar(x, draw_counts, bottom=[i+j for i,j in zip(win_counts, loss_counts)], color='b', label='Draws')
plt.bar(x, loss_counts, bottom=win_counts, color='r', label='Losses')
plt.xticks(x, openings, rotation='vertical')
plt.xlabel('Openings')
plt.ylabel('Number of Games')
plt.title(f'Game Results by Opening for {user}')
plt.legend()
plt.tight_layout()
plt.show()
ratios_per_opening={}
for opening in data:
    wins=data[opening][0]
    losses=data[opening][1]
    draws=data[opening][2]
    win_rate=wins/(wins+losses+draws) if (wins+losses+draws)>5 else 0
    loss_rate=losses/(wins+losses+draws) if (wins+losses+draws)>5 else 0
    draw_rate=draws/(wins+losses+draws) if (wins+losses+draws)>5 else 0
    ratios_per_opening[opening]=(win_rate, loss_rate, draw_rate)
    print(f"Opening: {opening}, Win Rate: {win_rate:.2f}, Loss Rate: {loss_rate:.2f}, Draw Rate: {draw_rate:.2f}")
    
#plot a pie chart of each one of the 5 best openings by win rate
top_openings=sorted(ratios_per_opening.items(), key=lambda x: x[1][0], reverse=True)[:5]
for opening, ratios in top_openings:
    if sum(ratios)==0:
        continue #security check to avoid plotting empty data
    labels = ['Wins', 'Losses', 'Draws']
    sizes = [ratios[0], ratios[1], ratios[2]]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Game Result Distribution for Opening: {opening}')
    plt.show()
    

 








