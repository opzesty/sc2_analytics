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
                    playerDict[player.toon_id] = {'playername': player.name, 'playerLarvaDelta': 0, 'playerLarvaTotal': 0}

            for event in replay.tracker_events:
                if isinstance(event, sc2reader.events.tracker.UnitBornEvent) and event.unit_type_name == 'Larva':
                    if event.control_pid == 1:
                        olarva[event.unit] = event.second
                    else:
                        tlarva[event.unit] = event.second


            ostats = 0
            ototal = 0
            omaxed = 0
            tstats = 0
            ttotal = 0
            tmaxed = 0

            for event in replay.tracker_events:
                if isinstance(event, sc2reader.events.tracker.PlayerStatsEvent) and event.food_used > 190:
                    if event.pid == 1 and omaxed != 1:
                        print("{}'s supply is basically maxed at {}/{}".format(event.player, event.food_used, event.food_made))
                        omaxed = 1
                    elif event.pid == 2 and tmaxed != 1:
                        print("{}'s supply is basically maxed at {}/{}".format(event.player, event.food_used, event.food_made))
                        tmaxed = 1

                if isinstance(event, sc2reader.events.tracker.UnitTypeChangeEvent) and event.unit in olarva and omaxed == 0:
                    morphingTime = event.second
                    bornTime = olarva[event.unit]
                    ostats += morphingTime-bornTime
                    ototal += 1
                elif isinstance(event, sc2reader.events.tracker.UnitTypeChangeEvent) and event.unit in tlarva and tmaxed == 0:
                    morphingTime = event.second
                    bornTime = tlarva[event.unit]
                    tstats += morphingTime-bornTime
                    ttotal += 1

            if ototal != 0:
                print("On average, larva born into {}'s army lived for {:.2f} game seconds until they were morphed to a higher form!".format(replay.player[1].name,ostats/ototal/1.4))
                playerDict[replay.player[1].toon_id]['playerLarvaDelta'] += ostats
                playerDict[replay.player[1].toon_id]['playerLarvaTotal'] += ototal
            if ttotal != 0:
                print("On average, larva born into {}'s army lived for {:.2f} game seconds until they were morphed to a higher form!".format(replay.player[2].name,tstats/ttotal/1.4))
                playerDict[replay.player[2].toon_id]['playerLarvaDelta'] += tstats
                playerDict[replay.player[2].toon_id]['playerLarvaTotal'] += ttotal

        for playerID, playerInfo in playerDict.items():
            if playerInfo['playerLarvaTotal'] != 0:
                print("{}'s average larva life (before max) across these games was: {:.2f}".format(playerInfo['playername'],playerInfo['playerLarvaDelta']/playerInfo['playerLarvaTotal']/1.4))
    except:
        pass

print ('Thank you, good bye!')
