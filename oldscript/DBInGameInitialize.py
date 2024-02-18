import sqlite3, csv
conn = sqlite3.connect("BackEndDB.db")
cursor = conn.cursor()

def CreateTblInGame():
    cursor.execute("""DROP TABLE IF EXISTS TblInGame""")
    cursor.execute("""CREATE TABLE TblInGame
                        (UnitID INTEGER PRIMARY KEY,
                         ModelID TEXT,
                         UnitSize INTEGER,
                         WeaponID TEXT,
                         Team INTEGER,
                         FOREIGN KEY (ModelID) REFERENCES TblModel(ModelID))""")
    txtfile = open("TblInGame.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblInGame VALUES (?, ?, ?, ?, ?)", i)
    txtfile.close()
    conn.commit()

CreateTblInGame()
