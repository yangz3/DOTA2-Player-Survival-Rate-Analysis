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
          'GameFinishRate', 'GameFrequency', 'GameHistory', 'NumberOfGame', 'NotPlaySinceLastGame', \
          'STDKills', 'STDDeaths', 'STDAssists', 'STDDuration', \
          'LWZKills','LWZDeaths','LWZAssists','LWZDuration', \
          'LMZKills','LMZDeaths','LMZAssists','LMZDuration', \
          'LWGameFrequency','LWWinningPercentage', 'LWGameFinishRate', \
          'LMGameFrequency','LMWinningPercentage', 'LMGameFinishRate'
          ]

body = [header,]
fileList = os.listdir('./download')

globalLastGameTime = 1524171363

weekSeconds = 604800
monthSeconds = 2419200

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

        NumberOfGame = 0 # total number of game that player has played

        LastDayDifference = 0
        LastWeekDifference = 0
        LastMonthDifference = 0
        
        
        NumberOfGame = len(data)
        heroSet = set()

  
        for d in data:
            st = d['start_time']


            if st < startTime:
                startTime = st

            if st > endTime:
                endTime = st
            
            
            AverageKills += float(d['kills'])/NumberOfGame
            AverageDeaths += float(d['deaths'])/NumberOfGame
            AverageAssists += float(d['assists'])/NumberOfGame
            AverageDuration += float(d['duration'])/NumberOfGame

            if (d['player_slot'] >> 3) == 0: #radiant
                if d['radiant_win'] == 1:
                    AverageWinningPercentage += 1.0/NumberOfGame
            else:
                if d['radiant_win'] == 0:
                    AverageWinningPercentage += 1.0/NumberOfGame

            heroSet.add(d['hero_id'])

            if d['leaver_status'] == 0:
                GameFinishRate += 1.0/NumberOfGame

        HeroSelectionDiversity = len(heroSet)
        
        
        if endTime - startTime != 0:
            GameHistory = float(endTime - startTime)/ 604800
            GameFrequency = 604800*float(NumberOfGame)/(endTime - startTime)
        else:
            GameHistory = 1
            GameFrequency = 1
        NotPlaySinceLastGame = float(globalLastGameTime - endTime)/604800

        if GameHistory > 8: # save data only if the user played for more than two months

            # calculating SD
            STDKills = 0
            STDDeaths = 0
            STDAssists = 0
            STDDuration = 0
            
            for r in data:
                STDKills += (float(r['kills'])- AverageKills)*(float(r['kills'])- AverageKills)/NumberOfGame
                STDDeaths += (float(r['deaths'])- AverageDeaths)* (float(r['deaths'])- AverageDeaths)/NumberOfGame
                STDAssists += (float(r['assists'])- AverageAssists)* (float(r['assists'])- AverageAssists)/NumberOfGame
                STDDuration += (float(r['duration'])- AverageDuration)* (float(r['duration'])- AverageDuration)/NumberOfGame
                
            STDKills = STDKills**0.5
            STDDeaths = STDDeaths**0.5
            STDAssists = STDAssists**0.5
            STDDuration = STDDuration**0.5

            # Calculating Last Week ZScores and Difference
            lastTime = data[0]['start_time']
            
            LWZKills = 0
            LWZDeaths = 0
            LWZAssists = 0
            LWZDuration = 0

            LWGameFrequency = 0
            LWWinningPercentage = 0
            LWGameFinishRate = 0
            weekCounter = 0
            
            for w in data:
                if w['start_time'] > lastTime - weekSeconds:
                    LWZKills += (float(w['kills']) - AverageKills)/STDKills
                    LWZAssists += (float(w['assists']) - AverageAssists)/STDAssists
                    LWZDeaths += (float(w['deaths']) - AverageDeaths)/STDDeaths
                    LWZDuration += (float(w['duration']) - AverageDuration)/STDDuration
                    weekCounter += 1.0
                    LWGameFrequency += 1.0

                    if (w['player_slot'] >> 3) == 0: #radiant
                        if w['radiant_win'] == 1:
                            LWWinningPercentage += 1.0
                    else:
                        if w['radiant_win'] == 0:
                            LWWinningPercentage += 1.0
                                  
                    if w['leaver_status'] == 0:
                        LWGameFinishRate += 1.0
                else:
                    break
                                  
                                  
            LWGameFinishRate = LWGameFinishRate/weekCounter
            LWWinningPercentage = LWWinningPercentage/weekCounter
            LWZDuration = LWZDuration/weekCounter
            LWZDeaths = LWZDeaths/weekCounter
            LWZAssists = LWZAssists/weekCounter
            LWZKills = LWZKills/weekCounter

            # Calculating Last Month ZScores and Difference
            LMZKills = 0
            LMZDeaths = 0
            LMZAssists = 0
            LMZDuration = 0

            LMGameFrequency = 0
            LMWinningPercentage = 0
            LMGameFinishRate = 0
            monthCounter = 0                   

            for m in data:
                if m['start_time'] > lastTime - monthSeconds:
                    LMZKills += (float(w['kills']) - AverageKills)/STDKills
                    LMZAssists += (float(w['assists']) - AverageAssists)/STDAssists
                    LMZDeaths += (float(w['deaths']) - AverageDeaths)/STDDeaths
                    LMZDuration += (float(w['duration']) - AverageDuration)/STDDuration
                    monthCounter += 1.0
                    LMGameFrequency += 1.0

                    if (m['player_slot'] >> 3) == 0: #radiant
                        if m['radiant_win'] == 1:
                            LMWinningPercentage += 1.0
                    else:
                        if m['radiant_win'] == 0:
                            LMWinningPercentage += 1.0
                                  
                    if m['leaver_status'] == 0:
                        LMGameFinishRate += 1.0
                    
                else:
                    break
                
            LMGameFinishRate = LMGameFinishRate/monthCounter
            LMWinningPercentage = LMWinningPercentage/monthCounter
            LMZDuration = LMZDuration/monthCounter
            LMZDeaths = LMZDeaths/monthCounter
            LMZAssists = LMZAssists/monthCounter
            LMZKills = LMZKills/monthCounter
            LMGameFrequency = LMGameFrequency / 4.0
                
            newRow = [UserID, AverageKills, AverageDeaths, AverageAssists, AverageDuration, AverageWinningPercentage, HeroSelectionDiversity, \
          GameFinishRate, GameFrequency, GameHistory, NumberOfGame, NotPlaySinceLastGame, \
                      STDKills, STDDeaths, STDAssists, STDDuration, \
          LWZKills,LWZDeaths,LWZAssists,LWZDuration, \
          LMZKills,LMZDeaths,LMZAssists,LMZDuration, \
          LWGameFrequency,LWWinningPercentage, LWGameFinishRate, \
          LMGameFrequency,LMWinningPercentage, LMGameFinishRate]
            
            body.append(newRow)

        
    except Exception as e:
        print e

with open ("./playerStats.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(body)

print 'done!'



        
    

    
        






