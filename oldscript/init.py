import sqlite3, pygame, random

conn = sqlite3.connect("BackEndDB.db")
cursor = conn.cursor()

back = pygame.image.load("boardbackdesert.png")

TerrainDict = {"bunker1": "1bunker_1x1.png",
               "bunker2": "2bunker_1x2.png",
               "bunker3": "3bunker_2x1.png",
               "bunker4": "4bunker_round_2x1.png",
               "bunker5": "5bunker_round_2x1.png",
               "bunker6": "6bunker_round.png",
               "bunker7": "7bunker_round.png",
               "bunker8": "8bunker_big.png"}

BaseDict = {"WARRIO": "OverlordBase.png",
            "OVERLO": "OverlordBase.png",
            "DESLOR": "DestroyerLordBase.png",
            "CRYPTE": "OverlordBase.png"}


class TerrainGroup(pygame.sprite.Group):

    def __init__(self, Surface):
        pygame.sprite.Group.__init__(self)
        self.Surface = Surface

    def createterrain(self):
        TerrainList = ["bunker1", "bunker2", "bunker3", "bunker4", "bunker5", "bunker6", "bunker7", "bunker8"]
        random.shuffle(TerrainList)
        for i in range(0, random.randint(3, 5)):
            self.add(TerrainPiece(self.Surface, TerrainList[i]))
        for i in self.sprites():
            i.image = pygame.transform.rotate(i.image, random.randint(0, 360))
            i.updaterect()
            i.rect.x = random.randint(50, 620)
            i.rect.y = random.randint(60, 420)


class TerrainPiece(pygame.sprite.Sprite):

    def __init__(self, Surface, TerrainID):
        pygame.sprite.Sprite.__init__(self)
        self.surface = Surface
        self.image = pygame.image.load(TerrainDict[TerrainID])
        self.rect = self.image.get_rect()

    def updaterect(self):
        self.rect = self.image.get_rect()


class model(pygame.sprite.Sprite):

    def __init__(self, surface, ModelID):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.image = pygame.image.load(BaseDict[ModelID])
        self.rect = self.image.get_rect()
        self.mGroup = pygame.sprite.Group()
        self.cGroup = pygame.sprite.Group()
        ModelIDlist = [ModelID]
        cursor.execute('''
        SELECT TblModel.Modelname, TblModel.M, TblModel.WS, TblModel.BS, TblModel.S, TblModel.T, TblModel.W, TblModel.A, TblModel.Ld, TblModel.Sv, TblModel.ISv FROM TblModel
        WHERE TblModel.ModelID = ?''', (ModelIDlist))
        row = cursor.fetchall()
        for x in row:
            self.ModelID = ModelID
            self.Modelname = x[0]
            self.M = x[1]
            self.WS = x[2]
            self.BS = x[3]
            self.S = x[4]
            self.T = x[5]
            self.W = x[6]
            self.A = x[7]
            self.Ld = x[8]
            self.Sv = x[9]
            self.ISv = x[10]

    def modelmove(self):
        print("modelmove begun")
        moved = False
        while not moved:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print("mouse registered")
                    print(event.pos)
                    self.rect.center = event.pos
                    self.mGroup.add(movementcircle(self.surface, self))
                    self.cGroup.add(coherencycircle(self.surface, self))
                    moved = True

                if event.type == pygame.QUIT:
                    print("quit exception raised")
                    pygame.quit()
                    quit()




class movementcircle(pygame.sprite.Sprite):

    def __init__(self, surface, model):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.radius = model.M + 1
        self.pos = (self.radius * 10, self.radius * 10)
        self.color = [0, 253, 12]
        self.incolor = [174, 255, 168]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius*20, self.radius*20))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(60)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius*10), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius*10), 3)
        self.rect = self.image.get_rect()
        self.rect.center = model.rect.center


class coherencycircle(pygame.sprite.Sprite):

    def __init__(self, surface, model):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.model = model
        self.radius = 3
        self.pos = (self.radius*10), (self.radius*10)
        self.color = [0, 225, 255]
        self.incolor = [142, 241, 255]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius*20, self.radius*20))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(60)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius*10), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius*10), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (model.rect.center)

    def update(self):
        self.rect.center = self.model.rect.center


class coherencygroup(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)


class unit(pygame.sprite.Group):

    def __init__(self, surface, id, team, size):
        pygame.sprite.Group.__init__(self)
        self.surface = surface
        self.id = id
        self.idlist = [id]
        self.team = team
        self.size = size
        self.cGroup = coherencygroup()

    def unitmove(self):
        for i in self.sprites():
            print("starting modelmove")
            i.modelmove()

    def createmodels(self):
        cursor.execute('''
        SELECT TblInGame.ModelID FROM TblInGame
        WHERE TblInGame.UnitID = ?''', self.idlist)
        row = cursor.fetchall()
        for i in range(0, self.size):
            for x in row:
                self.add(model(self.surface, x[0]))


def create_connection(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return cursor


class player:

    def __init__(self, surface, playerID,  team):
        self.surface = surface
        self.playerID = playerID
        self.team = [team]
        self.units = []
        self.modellist = []
        self.VP = 0

    def createunits(self):
        cursor.execute('''
        SELECT TblInGame.UnitID, TblInGame.Team, TblInGame.UnitSize FROM TblInGame
        WHERE TblInGame.Team = ?''', self.team)
        row = cursor.fetchall()
        for x in row:
            self.units.append(unit(self.surface, x[0], x[1], x[2]))
        print(self.units)
        for i in range(0, len(self.units)):
            self.units[i].createmodels()
