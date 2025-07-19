from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from spotifyapi import get_song

Base = declarative_base() # Base is a class that will track all of the tables we create and allows us to create new tables by subclassing it.

#create a new table called "users":
class User(Base):
    __tablename__ = 'Users'
    #now we create each of the columns
    # [COLUMN NAME] = Column([DATA TYPE], [FLAGS])
    id = Column(Integer, primary_key=True)
    img = Column(String, nullable=False)
    name = Column(String, nullable=False)
    song_url = Column(String)
    song_cover_url = Column(String)
    song_artist = Column(String)
    song_name = Column(String)
    light_color = Column(String) # json for r, g, and b


# define the "engine" which acts as the python representation of the SQLite file.
engine = create_engine('sqlite:///hestia.db', echo=True)

#define the Session which actually performs CRUD
#bind tells the session maker which DB file we want to work on
Session = sessionmaker(bind=engine)
#Session is a class that we get from session_maker (called a Python Factory), which we then create an instance of on the line below this comment
session = Session()


#looks at all of the subclasses of Base (a.k.a all the tables we've created) and issues sqlite CREATE_TABLE commands if they don't already exist.
Base.metadata.create_all(engine)


# functions to be called by other programs
def add_user(img, name, song_url='',light_color='255'):
    # if user does not already exist, create them
    if session.query(User).filter_by(name=name).first() == None:
        song_name, song_artist, song_cover_url = get_song(song_url)
        user_to_add = User(img=img, name=name, song_url=song_url, song_cover_url=song_cover_url, song_artist=song_artist, song_name=song_name, light_color=light_color)
        session.add(user_to_add)
        session.commit()

def update_user(uname, **kwargs):
    user = session.query(User).filter_by(name=uname).first()
    if 'song_url' in kwargs.keys():
        user.song_url = kwargs['song_url']
    if 'light_color' in kwargs.keys():
        user.light_color = kwargs['light_color']
    session.commit()

def get_user(name):
    result = session.query(User).filter_by(name=name).first()
    if result == None:
        raise ValueError('User not found')
    else:
        return result

def del_user(name):
    session.delete(session.query(User).filter_by(name=name).first())
    session.commit()


def get_all_users():
    return session.query(User).all()


# *** CRUD stuff! ***
# Create
#luka = User(name='Luka', song_url='https://open.spotify.com/album/32ium7Cxb1Xwp2MLzH2459?si=o5UbpXJfRmqVs8gKCr5b4Q', light_color='255')
#session.add(luka)
##commit changes!
#session.commit()
#
## Read
## User is the class representing the User table. 
#users = session.query(User).all() # list all
#
## filter_by(name='Luka') is a method that uses the kwarg of name='luka' to construct a SQL query like this:
## SELECT * FROM users WHERE name = 'Luka'
## the .first() retrieves only the first row.
#luka_user = session.query(User).filter_by(name='Luka').first()
#luka_song = luka_user.song_url
#print('Luka\'s song:',luka_song) #
## Update
#
#luka_user.name = 'marica'
#session.commit()
#print('The name is now', luka_user.name)
#
## Delete
#
#session.delete(luka_user)
#session.commit()




