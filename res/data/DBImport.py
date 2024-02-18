import csv, sqlite3

conn = sqlite3.connect("BackEndDB.db")
cursor = conn.cursor()


def CreateTblModel():
    cursor.execute("""CREATE TABLE TblModel
                    (ModelID TEXT PRIMARY KEY ,
                    Faction TEXT,
                    Keywords TEXT,
                    Modelname TEXT,
                    M INTEGER,
                    WS INTEGER,
                    BS INTEGER,
                    S INTEGER,
                    T INTEGER,
                    W INTEGER,
                    A INTEGER,
                    Ld INTEGER,
                    Sv INTEGER,
                    ISv INTEGER,
                    Abilities INTEGER)""")
    txtfile = open("TblModel.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblModel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
    txtfile.close()
    conn.commit()


def CreateTblWargear():
    cursor.execute("""CREATE TABLE TblWargear
                    (WargearID TEXT PRIMARY KEY ,
                    WargearName TEXT,
                    Effect TEXT)""")
    txtfile = open("TblWargear.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblWargear VALUES (?, ?, ?)", i)
    txtfile.close()
    conn.commit()


def CreateTblWargearInModel():
    cursor.execute("""CREATE TABLE TblWargearInModel
                    (ID INTEGER PRIMARY KEY ,
                    ModelID TEXT,
                    WargearID TEXT,
                    FOREIGN KEY (ModelID) REFERENCES TblModel(ModelID),
                    FOREIGN KEY (WargearID) REFERENCES TblWargear(WargearID))""")
    txtfile = open("TblWargearInModel.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblWargearInModel VALUES (?, ?, ?)", i)
    txtfile.close()
    conn.commit()


def CreateTblWeapon():
    cursor.execute("""CREATE TABLE TblWeapon
                    (WeaponID TEXT PRIMARY KEY ,
                    Type TEXT,
                    RorM TEXT,
                    Shots TEXT,
                    Range INTEGER,
                    S INTEGER,
                    AP INTEGER,
                    D TEXT,
                    Abilities TEXT)""")
    txtfile = open("TblWeapon.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblWeapon VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
    txtfile.close()
    conn.commit()


def CreateTblWeaponInModel():
    cursor.execute("""CREATE TABLE TblWeaponInModel
                    (ID TEXT PRIMARY KEY ,
                    ModelID TEXT,
                    WeaponID TEXT,
                    FOREIGN KEY (ModelID) REFERENCES TblModel(ModelID),
                    FOREIGN KEY (WeaponID) REFERENCES TblWeapon(WeaponID))""")
    txtfile = open("TblWeaponInModel.txt", "r")
    creader = csv.reader(txtfile, delimiter="|")
    for i in creader:
        cursor.execute("INSERT INTO TblWeaponInModel VALUES (?, ?, ?)", i)
    txtfile.close()
    conn.commit()


def InitializeBackEndDB():
    CreateTblModel()
    CreateTblWargear()
    CreateTblWargearInModel()
    CreateTblWeapon()
    CreateTblWeaponInModel()


InitializeBackEndDB()
