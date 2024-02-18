import sqlite3

conn = sqlite3.connect("BackEndDB.db")
cursor = conn.cursor()

ModelIDlist = ["OVERLO"]

def JoinModelWeaponWargearSearch():

    cursor.execute('''
SELECT TblModel.ModelID,
TblModel.Modelname, TblWeapon.WeaponID, TblWeapon.S, TblWeapon.AP
FROM TblModel
INNER JOIN TblWeaponInModel ON TblModel.ModelID = TblWeaponInModel.ModelID
INNER JOIN TblWeapon ON TblWeapon.WeaponID = TblWeaponInModel.WeaponID
WHERE TblModel.ModelID = ?''', (ModelIDlist))
    row = cursor.fetchall()
    for x in row:
        print("Model ID = ",x[0])
        print("Model name = ",x[1])
        print("Weapon ID = ",x[2])
        print("Weapon strength = ", x[3])
        print("Weapon AP = ",x[4],"\n")

JoinModelWeaponWargearSearch()

def characteristicstest():

    cursor.execute('''SELECT
TblModel.ModelID,
TblModel.Modelname,
TblModel.M,
TblModel.WS,
TblModel.BS,
TblModel.S,
TblModel.T,
TblModel.W,
TblModel.A,
TblModel.Ld,
TblModel.Sv
FROM TblModel
WHERE TblModel.ModelID = "WARRIO"''')
    row = cursor.fetchall()
    for x in row:
        print(x[0])
        print(x[1])
        print(x[2])
        print(x[3])
        print(x[4])
        print(x[5])
        print(x[6])
        print(x[7])
        print(x[8])
        print(x[9])
        print(x[10])

def weapontest():

    cursor.execute('''SELECT
TblWeapon.WeaponID,
TblWeapon.Range,
TblWeapon.Type,
TblWeapon.Shots,
TblWeapon.S,
TblWeapon.AP,
TblWeapon.D
FROM TblWeapon
WHERE TblWeapon.WeaponID = "GAUSSFLAYER"''')
    row = cursor.fetchall()
    for x in row:
        print(x[0])
        print(x[1])
        print(x[2])
        print(x[3])
        print(x[4])
        print(x[5])
        print(x[6])

def wargeartest():
    cursor.execute('''SELECT
TblWargear.WargearID,
TblWargear.WargearName,
TblWargear.Effect
FROM TblWargear
WHERE TblWargear.WargearID = "PHYLACTERY"''')
    row = cursor.fetchall()
    for x in row:
        print(x[0])
        print(x[1])
        print(x[2])
