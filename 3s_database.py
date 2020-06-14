from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)

metadata = MetaData()
Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    toon_ids = relationship("Toon_Id")

class Toon_Id(Base):
    __tablename__ = 'toon_id'
    toon_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))

class Stat_Type(Base):
    __tablename__ = 'stat_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Stat(Base):
    __tablename__ = 'stat'
    id = Column(Integer, primary_key=True)
    stat_type_id = relationship("Stat_Type")
    player_id = relationship("Player")
    replay_id = relationship("Replay")
    value = Column(String)

class Replay(Base):
    __tablename__ = 'replay'
    #shouldn't the primary key be the replay hash?
    id = Column(Integer, primary_key=True)
    #should this be an Integer, or a hexadecimal value?
    replay_hash = Column(String)
    #maybe should import date and make this that?
    date_time = Column(String)
    teams = relationship("Team")

#I'm not sure what the primary key is supposed to be here....is there one?
class Team(Base):
    __tablename__ = 'team'
    replay_id = relationship("Replay")
    team_name_id = relationship("Team_Name")
    place = Column(Integer)
    players = relationship("Player")

#I honestly don't remember what this table is for
class Team_Name(Base):
    __tablename__ = 'team_name'
    id = Column(Integer, primary_key=True)
    name = Column(String)

#this language stuff is pretty convulted to me.  I doubt I did this right

class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    english_name = Column(String)
    names = relationship("Race_Language")

class Race_Language(Base):
    __tablename__ = 'race_language'
    id = Column(Integer, primary_key=True)
    #or should race_id be an integer?
    race_id = relationship("Race")
    language_id = relationship("Language")
    word = Column(String)

class Language(Base):
    __tablename__ = 'langauge'
    id = Column(Integer, primary_key=True)
    name = Column(String)
