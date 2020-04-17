import sc2reader
import os
import datetime
import yaml


with open("US_Excelle.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)

print("Loading replays from: " + cfg["replay_path"])

response = ['']
playerDict = {}

def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

while response != 'exit':
    try:
        response = input("Input day to calculate replay analysis time from in format \"YYYYmmDD\" (or exit): ")
        path = cfg["replay_path"] + response
        replays = sc2reader.load_replays(path, load_level=4)



        for replay in replays:
            olarva = {}
            tlarva = {}

            print("   Map:      {0}".format(replay.map_name))
            print("   Length:   {0} minutes".format(replay.game_length))
            print("   Date:     {0}".format(replay.start_time))
            lineups = [team.lineup for team in replay.teams]
            print("   Matchup:    {0}".format("v".join(lineups)))

            for team in replay.teams:
                print("   Player {0}\t{1}".format(team.number, team.players[0]))


            for player in replay.players:
                if player.toon_id not in playerDict:
                    playerDict[player.toon_id] = {'playername': player.name, 'resourcesLostTotal': 0, 'resourcesLostCount': 0}

            oResourcesLost = 0
            tResourcesLost = 0

            for event in replay.tracker_events:
                if isinstance(event, sc2reader.events.tracker.PlayerStatsEvent):
                    if event.pid == 1 and event.second % 60 == 0:
                        print("{}'s resources lost @ {:.0f}: {:.2f}".format(event.player, event.second/1.4, event.resources_lost))
                        oResourcesLost = event.resources_lost
                    elif event.pid == 2 and event.second % 60 == 0:
                        print("{}'s resources lost @ {:.0f}: {:.2f}".format(event.player, event.second/1.4, event.resources_lost))
                        tResourcesLost = event.resources_lost

            if tResourcesLost != 0:
                print("{}'s resources lost to opponents: {:.0f}/{:.0f} ({:.2f})".format(replay.player[1].name,oResourcesLost,tResourcesLost,oResourcesLost/tResourcesLost))
                playerDict[replay.player[1].toon_id]['resourcesLostTotal'] += oResourcesLost/tResourcesLost
                playerDict[replay.player[1].toon_id]['resourcesLostCount'] += 1
            else:
                print("{} did not lose any resources, so can not calculate ratio for {}".format(replay.player[2],replay.player[1]))

            if oResourcesLost != 0:
                print("{}'s resources lost to opponents: {:.0f}/{:.0f} ({:.2f})".format(replay.player[2].name,tResourcesLost,oResourcesLost,tResourcesLost/oResourcesLost))
                playerDict[replay.player[2].toon_id]['resourcesLostTotal'] += tResourcesLost/oResourcesLost
                playerDict[replay.player[2].toon_id]['resourcesLostCount'] += 1
            else:
                print("{} did not lose any resources, so can not calculate ratio for {}".format(replay.player[1],replay.player[2]))


        for playerID, playerInfo in playerDict.items():
            if playerInfo['resourcesLostTotal'] != 0:
                print("{}'s average resource lost ratio across these games was: {:.4f}".format(playerInfo['playername'],playerInfo['resourcesLostTotal']/playerInfo['resourcesLostCount']))
    except:
        pass

print ('Thank you, good bye!')
