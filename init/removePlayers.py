import sqlite3

conn = sqlite3.connect('DB.db')
c = conn.cursor()
c.execute("DELETE FROM Players")
conn.commit()
conn.close()
