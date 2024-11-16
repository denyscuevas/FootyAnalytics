import json
from understatapi import UnderstatClient

from fastapi import FastAPI
app = FastAPI()
understat = UnderstatClient()


@app.get("/")
def main():
    return "HELLO THERE"

@app.get("/get-teamData")
def getTeamsData(): 
    # can either just retrieve team names or i can do that manually as is only 3 changes each season
    # can change this to just be team data (shots, passes, etc..)
    
    
    #this returns strictly teamNames
    teams = understat.league("EPL").get_team_data("2024")
    return teams


@app.get("/get-players")
#get players can either get all players or get players from a specific team
def getPlayersFromTeam(teamName : str):
    if teamName != "any":
        #requested players from teamName
        # if the string is equal to a teamName find players from that given team
        choseTeam = understat.team(team=teamName)
        return choseTeam.get_player_data("2024")
    else:
        #requested all players
        players = understat.league("EPL").get_player_data("2024")
        return players
    

@app.get("/player-data")
# get match data from a specific game
def getPlayerData(playerName : str, season : str):
    # getPlayerData such as shot data, match-data, season-data
    # have got to get playerID
    
    playerID = None
    for player in getPlayersFromTeam("any"):
        #get players in the 2024 season
        if player["player_name"] == playerName:
            playerID = player["id"]
    
    if playerID:
        shotData = understat.player(playerID).get_shot_data()
    else:
        return "NOT FOUND"
    
    seasonShotData = []
    
    for data in shotData:
        if data["season"] == season :
            seasonShotData.append(data)
    return seasonShotData

	
