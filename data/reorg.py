import json
import os
import csv

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




header = ['UserID', 'AverageKills', 'AverageDeaths', 'AverageAssists', 'AverageDuration', 'AverageWinningPercentage', 'HeroSelectionDiversity', \
          'GameFinishRate', 'GameFrequency', 'GameHistory', 'NumerOfGame', 'NotPlaySinceLastGame']

body = [header,]
fileList = os.listdir('./download')

globalLastGameTime = 1524171363

for fn in fileList:

    try:
        if (not fn.endswith('.json')):
            pass
        #print fn
        data = json.load(open('./download/' + fn))

        startTime = 9999999999
        endTime = 0

        UserID = fn.split('_')[0]
        #print data[0]

        AverageKills = 0
        AverageDeaths = 0
        AverageAssists = 0
        AverageDuration = 0
        
        AverageWinningPercentage = 0
        HeroSelectionDiversity = 0 # number of different heros used 
        GameFinishRate = 0 # percentage of finished game
        GameFrequency = 0 # how many games per week
        GameHistory = 0 # the player has been playing for how many weeks
        NotPlaySinceLastGame = 0 # how many weeks the player has not played since last game

        NumerOfGame = 0 # total number of game that player has played

        
        NumerOfGame = len(data)
        heroSet = set()
        
        for d in data:
            st = d['start_time']

            if st < startTime:
                startTime = st

            if st > endTime:
                endTime = st
            
            
            AverageKills += float(d['kills'])/NumerOfGame
            AverageDeaths += float(d['deaths'])/NumerOfGame
            AverageAssists += float(d['assists'])/NumerOfGame
            AverageDuration += float(d['duration'])/NumerOfGame

            if (d['player_slot'] >> 3) == 0: #radiant
                if d['radiant_win'] == 1:
                    AverageWinningPercentage += 1.0/NumerOfGame
            else:
                if d['radiant_win'] == 0:
                    AverageWinningPercentage += 1.0/NumerOfGame

            heroSet.add(d['hero_id'])

            if d['leaver_status'] == 0:
                GameFinishRate += 1.0/NumerOfGame

        HeroSelectionDiversity = len(heroSet)
        GameHistory = float(endTime - startTime)/ 604800
        GameFrequency = 604800*float(NumerOfGame)/(endTime - startTime)
        NotPlaySinceLastGame = float(globalLastGameTime - endTime)/604800

        newRow = [UserID, AverageKills, AverageDeaths, AverageAssists, AverageDuration, AverageWinningPercentage, HeroSelectionDiversity, \
          GameFinishRate, GameFrequency, GameHistory, NumerOfGame, NotPlaySinceLastGame]

        body.append(newRow)

        
    except Exception as e:
        print e

with open ("./playerStats.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(body)

print 'done!'



        
    

    
        






