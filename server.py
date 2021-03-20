from yahoo_oauth import OAuth2
import sys

import json
import yahoo_fantasy_api as yfa
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS, cross_origin
import os

from operator import itemgetter
import subprocess
import _pickle as cPickle


oauth = OAuth2(None, None, from_file='oauth2.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

gm = yfa.Game(oauth, 'nba')
lg = gm.to_league('402.l.67232')


app = Flask(__name__)
cors = CORS(app)
statMap = {"5": "FG%", "8":"FT%", "10":"3PTM", "12":"PTS", "15":"REB", "16":"AST", "17":"ST", "18":"BLK", "19":"TO"}

@app.route('/')
@cross_origin()
def index():
    return ""

@app.route('/matchups', methods=['GET'])
@cross_origin()
def getMatchups():
    
    matchupInfo = lg.matchups()

    return matchupInfo

    

@app.route('/win-calculator', methods=['POST'])
@cross_origin()
def getWins():

    data = json.loads(request.form.get("data"))
    
    
    categoryMax = {"FG%":{}, "FT%":{}, "3PTM":{},"PTS":{}, "REB":{}, "AST":{}, "ST":{}, "BLK":{}, "TO":{}}
    
    for x in data:
        
        for y in list(x.keys()): #team stats
            
            for z in x[y].keys(): #cats
                categoryMax[z][y] = float(x[y][z])

    catSort = {}
    for x in categoryMax:
        sortedCategory = (sorted(categoryMax[x].items(), key=itemgetter(1), reverse=True))
        catSort[x] = sortedCategory

        

                
    return catSort
    
@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    
    teams = {}

    matchupInfo = lg.matchups()
    data = matchupInfo["fantasy_content"]["league"][1]["scoreboard"]["0"]["matchups"]
    
                
    matchupKey = data.keys()

    current = ""
    for y in range(0,6):
        for z in range(0,2):
            for q in data[str(y)]["matchup"]["0"]["teams"][str(z)]["team"]:
                if (isinstance(q, list)):
                    teams[q[2]["name"]] = {}
                    current = q[2]["name"]
            for x in data[str(y)]["matchup"]["0"]["teams"][str(z)]["team"][1]["team_stats"]["stats"]:
                try:
                    teams[current][(statMap[x["stat"]["stat_id"]])] = x["stat"]["value"]
                except:
                    continue

    return teams

@app.route('/winning-matchups', methods=['POST'])
@cross_origin()
def winning():
    data = json.loads(request.form.get("data"))
    currentWins = {}

    for x in data:
        for player1 in list(x.keys()): #team stats
            currentWins[player1] = []
            for y in data:
                for player2 in list(y.keys()):
                    
                    if (player1 == player2):
                        continue
                    
                    winCount = 0
                    catWins = []
                    
                    if (float(x[player1]['TO']) < float(y[player2]['TO'])):
                        winCount+=1
                        catWins.append('TO')
                    for z in x[player1].keys(): #cats
                        
                        if (float(x[player1][z]) > float(y[player2][z]) and z != 'TO'):
                            winCount+=1
                            catWins.append(z)


                    if (winCount >= 5):
                                print(catWins)
                                currentWins[player1].append({player2: catWins}) 

                                
                            

                        
                        
                        
    
    return currentWins

   

if __name__ == '__main__':
    dev = False
    portVar = ""
    if (dev):
        portVar = 8000
    else:
        portVar = os.environ.get('PORT', 80)
    app.run(host="localhost", port=portVar, debug=dev)