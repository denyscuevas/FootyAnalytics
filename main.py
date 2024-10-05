from understatapi import UnderstatClient

from fastapi import FastAPI
app = FastAPI()
understat = UnderstatClient()

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
    

@app.get("/match-data")
# get match data from a specific game
def getMatchData(playerName : str):
    # getMatchData will be able to get either match data from the game itself 
    # or from a specific player specified by the client
    #
    if playerName == "any":
        #we want to return match data
        data = understat.league("EPL").get_match_data("2024")
    else:
        #we want to return specific player match data
        for player in getPlayersFromTeam("any"):
            if player["player_name"] == playerName:
                data = player

    
    return data
