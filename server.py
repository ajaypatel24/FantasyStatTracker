from yahoo_oauth import OAuth2
import sys

import json
import yahoo_fantasy_api as yfa
from flask import Flask, request, jsonify, redirect
import os

from operator import itemgetter
import subprocess
import _pickle as cPickle

sys.path.append(os.path.abspath(os.path.join('../', 'cred')))
from credentials import *

cred = {}
with open ('/Users/ajaypatel/Desktop/cred/credentials.py', "r") as r:
    cred = r.readline()

print(cred)

'''
with open('oauth2.json', "w") as f:
        f.write(json.dumps(creds))
        '''
oauth = OAuth2(None, None, from_file='oauth2.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

print(oauth)


gm = yfa.Game(oauth, 'nba')
lg = gm.to_league('402.l.67232')
print(gm.league_ids(year=2020))
    

app = Flask(__name__)
statMap = {"5": "FG%", "8":"FT%", "10":"3PTM", "12":"PTS", "15":"REB", "16":"AST", "17":"ST", "18":"BLK", "19":"TO"}
@app.route('/')
def index():
    return ""

@app.route('/auth/yahoo', methods=['GET']) 
def auth():
    authorizationUrl = 'https://api.login.yahoo.com/oauth2/request_auth'

    q = {
        "client_id": 'dj0yJmk9ZG9IajI1b05PZ1hCJmQ9WVdrOWVXOHpVMk53Tm04bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTU4',
        "redirectUri": 'http://localhost:8000/auth/yahoo/callback',
        "response_type": 'code'
    }

    return redirect(authorizationUrl + '?' + json.stringify(q))

@app.route('/matchups', methods=['GET'])
def getMatchups():
    f = open("output.json", "w")
    matchupInfo = lg.matchups()
    json.dump(matchupInfo, f)

    f.close()
    
    subprocess.call("./sendfile.sh")

    return "Deployed Updated Data"

    

@app.route('/win-calculator', methods=['POST'])
def getWins():

    data = json.loads(request.form.get("data"))
    
    
    categoryMax = {"FG%":{}, "FT%":{}, "3PTM":{},"PTS":{}, "REB":{}, "AST":{}, "ST":{}, "BLK":{}, "TO":{}}
    
    for x in data:
        
        for y in list(x.keys()): #team stats
            
            for z in x[y].keys(): #cats
                categoryMax[z][y] = float(x[y][z])

    catSort = {}
    for x in categoryMax:
        print(categoryMax[x])
        sortedCategory = (sorted(categoryMax[x].items(), key=itemgetter(1), reverse=True))
        catSort[x] = sortedCategory
        print(catSort)
        

                
    return catSort
    
@app.route('/test', methods=['GET'])
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
def winning():
    data = json.loads(request.form.get("data"))
    currentWins = {}
    print(data)

    for x in data:
        for player1 in list(x.keys()): #team stats
            currentWins[player1] = []
            for y in data:
                for player2 in list(y.keys()):
                    if (player1 == player2):
                        continue
                    
                    winCount = 0
                    for z in x[player1].keys(): #cats
                        
                        if (winCount >= 5):
                            currentWins[player1].append(player2) 
                            break
                        if (x[player1][z] > y[player2][z]):
                            winCount+=1
                        
    return currentWins

   

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)