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

def display_human_time(time):
    return datetime.timedelta(microseconds=delta.microseconds)

def normalize_sc2_time(game_time):
    real_time = game_time / 1.4
    return real_time

def identify_zvp(replay_list):
    zvp_replays = []
    for replay in replay_list:
        try:
            if replay.player[1].play_race == "Protoss":
                if replay.player[2].play_race == "Zerg":
                    zvp_replays.append(replay)
            elif replay.player[1].play_race == "Zerg":
                if replay.player[2].play_race == "Protoss":
                    zvp_replays.append(replay)
        except:
            pass
    return zvp_replays

try:
    path = os.path.normpath(cfg["replay_path"])
    replays = sc2reader.load_replays(path, load_level=4)

    zvp_replays = identify_zvp(replays)

    for replay in zvp_replays:
        try:
            print("Potential Cannon rush Game!: {} vs {}".format(replay.player[1], replay.player[2]))
        except:
            print("failed to display potential game")
            pass

    for replay in zvp_replays:
        try:
            for event in replay.events:
                if isinstance(event, sc2reader.events.tracker.UnitInitEvent) and event.unit_type_name == "Forge" and normalize_sc2_time(event.second) < 120:
                    print("Replay Name: {}".format(replay.filename))
                    print("Player1: {} vs Player2: {}".format(replay.player[1], replay.player[2]))
                    print("{}: {}".format(str(datetime.timedelta(seconds = normalize_sc2_time(event.second))), event.unit_type_name))
        except:
            print("failed to display potential game")
            pass

    print("finished finding cannon rushes!")
except Exception as err:
    print(err)
    pass
