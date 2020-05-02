import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


print("Your SQLAlchemy version is v. {}.".format(sqlalchemy.__version__))

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)

print("\n.__getstate__ \n{}".format(User.__table__.__getstate__))


print("\n\n\n")
Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print("ed_user name: {}, nickname: {} and id: {}".format(ed_user.name,ed_user.nickname,str(ed_user.id)))

Session = sessionmaker(bind=engine)
session = Session()
session.add(ed_user)
