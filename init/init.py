import sqlite3

conn = sqlite3.connect('DB.db')
c = conn.cursor()

# Drop all tables if exists
c.execute("DROP TABLE IF EXISTS Players")
c.execute("DROP TABLE IF EXISTS Channels")
c.execute("DROP TABLE IF EXISTS PrivateDatas")
c.execute("DROP TABLE IF EXISTS Messages")

# Create PLayers
c.execute('''CREATE TABLE Players
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
             Firstname TEXT NOT NULL,
             Lastname TEXT NOT NULL,
             Ranking TEXT NOT NULL,
             Club TEXT NOT NULL,
             Mail TEXT NOT NULL,
             SM INTEGER CHECK (SM IN (0,1)),
             SD INTEGER CHECK (SD IN (0,1)),
             DM INTEGER CHECK (DM IN (0,1)),
             DD INTEGER CHECK (DD IN (0,1)),
             DX INTEGER CHECK (DX IN (0,1)),
             C INTEGER CHECK (C IN (0,1)),
             State INTEGER CHECK (State IN (0,1)))''')

# Create Channels
c.execute('''CREATE TABLE Channels
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
             Category TEXT NOT NULL,
             ChannelId INTEGER)''')

# Create PrivateDatas
c.execute('''CREATE TABLE PrivateDatas
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
             Type TEXT NOT NULL,
             Data TEXT)''')

# Create Messages
c.execute('''CREATE TABLE Messages
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
             Category TEXT NOT NULL,
             Message TEXT)''')
conn.commit()
conn.close()
