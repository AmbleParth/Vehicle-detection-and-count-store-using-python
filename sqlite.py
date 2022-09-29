import sqlite3

conn = sqlite3.connect('count.db')

c = conn.cursor
c.execute("""CREATE TABLE count (
        count integer
)""")
c.execute("INSERT INTO count VALUES('?")

conn.commit()
conn.close()