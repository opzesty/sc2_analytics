from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db', echo=True)

metadata = MetaData()
Base = declarative_base()

player_team = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id')))

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Toon_Id(Base):
    __tablename__ = 'toon_id'
    toon_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("Player", backref="toon_ids")

class Stat_Type(Base):
    __tablename__ = 'stat_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Stat(Base):
    __tablename__ = 'stat'
    id = Column(Integer, primary_key=True)
    stat_type_id = Column("Integer", ForeignKey("stat_type.id"))
    stat_type = relationship("Stat_Type", backref="stats")
    player_id = Column("Integer", ForeignKey("player.id"))
    player = relationship("Player", backref="stats")
    replay_id = Column("Integer", ForeignKey("replay.id"))
    replay = relationship("Replay", backref="stats")
    value = Column(String)

class Replay(Base):
    __tablename__ = 'replay'
    replay_hash = Column(String, primary_key=True)
    date_time = DateTime(String)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    replay_id = Column("Integer", ForeignKey("replay.id"))
    replay = relationship("Replay", backref="teams")
    team_name_id = Column("Integer", ForeignKey("team_name.id"))
    team_name = relationship("Team_Name", backref="teams")
    place = Column(Integer)
    players = relationship("Player",
                    secondary=player_team,
                    backref="teams")

class Team_Name(Base):
    __tablename__ = 'team_name'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
if __name__ == "__main__":
    meta.create_all(engine)

