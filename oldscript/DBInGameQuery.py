import sqlite3

conn = sqlite3.connect("BackEndDB.db")
cursor = conn.cursor()
team = [2]
def TblInGameQuery():

    cursor.execute('''
SELECT TblInGame.UnitID, TblInGame.ModelID, TblModel.Modelname, TblInGame.WeaponID, TblInGame.Unitsize, TblInGame.Team  FROM TblInGame
INNER JOIN TblModel ON TblModel.ModelID = TblInGame.ModelID
WHERE TblInGame.Team = ?''', (team))
    row = cursor.fetchall()
    for x in row:
        print("Unit ID = ", x[0])
        print("Model ID = ", x[1])
        print("Model name = ", x[2])
        print("Weapon ID = ", x[3])
        print("Unit size = ", x[4])
        print("Team  = ", x[5],"\n")

TblInGameQuery()
