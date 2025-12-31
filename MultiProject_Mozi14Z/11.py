import sqlite3

# Add meg a teljes elérési utat a movies.db-hez
db_path = r"C:\Users\lacos\PycharmProjects\MultiProject_Mozi14X\movies.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Ellenőrizzük a users tábla oszlopait
c.execute("PRAGMA table_info(users);")
print(c.fetchall())

# Teszt: token frissítése egy userhez
token = "teszt_token_123"
c.execute("UPDATE users SET password_reset_token=? WHERE username=?", (token, "lacos0333"))
conn.commit()
conn.close()
print("Token frissítve!")
