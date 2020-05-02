import sc2reader

path = './replays/20200416Game 5.SC2Replay'

replay = sc2reader.load_replay(path, load_level=4)


for player in replay.players:
    print(player)

for event in replay.events: 
#    if isinstance(event, sc2reader.events.tracker.UnitInitEvent) or isinstance(event, sc2reader.events.tracker.UnitDoneEvent) or isinstance(event, sc2reader.events.tracker.UpgradeCompleteEvent):
    print("{} Time: {:.2f}".format(event,event.second/1.4))
