import pygame
import random
import sqlite3
from math import sqrt


def pickplayer(playerlist):
    random.shuffle(playerlist)
    return playerlist


def turnstart(playerlist, turn):
    for i in range(0, 100):
        print(pickplayer(playerlist)[0])


def movephase(currentplayer):
    for i in currentplayer.units:
        i.unitmove()


def deploy(playerlist):
    for player in playerlist:
        print("Player", player.team[0], "is now deploying")
        player.deploy()
        player.dGroup.empty()


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


class chargecircle(pygame.sprite.Sprite):
    def __init__(self, Surface, model):
        pygame.sprite.Sprite.__init__(self)
        self.surface = Surface
        self.model = model
        self.radius = 120 + int(self.model.radius)
        self.pos = (self.radius, self.radius)
        self.color = [255, 0, 102]
        self.incolor = [255, 76, 147]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(60)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius), 3)
        self.rect = self.image.get_rect()
        self.rect.center = model.rect.center

    def update(self):
        self.rect.center = self.model.rect.center


class chargegroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.state = False


class weapon():
    def __init__(self, model, WeaponID, Type, RorM, Shots, Range, S, AP, D):
        self.WeaponID = WeaponID
        self.Type = Type
        self.RorM = RorM
        self.Shots = Shots
        self.Range = Range
        self.S = S
        self.AP = AP
        self.D = D


class model(pygame.sprite.Sprite):
    def __init__(self, surface, ModelID):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.image = pygame.image.load(BaseDict[ModelID])
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.5
        self.mGroup = movementgroup()
        self.rGroup = rangegroup()
        self.mrGroup = rangegroup()
        self.chGroup = chargegroup()
        self.chGroup.add(chargecircle(surface, self))
        self.temp = 0
        self.Mweapon = None
        self.Rweapon = None
        ModelIDlist = [ModelID]
        cursor.execute('''
        SELECT TblModel.Modelname,
        TblModel.M,
        TblModel.WS,
        TblModel.BS,
        TblModel.S,
        TblModel.T,
        TblModel.W,
        TblModel.A,
        TblModel.Ld,
        TblModel.Sv,
        TblModel.ISv
        FROM TblModel
        WHERE TblModel.ModelID = ?''', (ModelIDlist))
        mrow = cursor.fetchall()
        for x in mrow:
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
        cursor.execute('''
                SELECT TblWeapon.WeaponID,
                TblWeapon.Type,
                TblWeapon.RorM,
                TblWeapon.Shots,
                TblWeapon.Range,
                TblWeapon.S,
                TblWeapon.AP,
                TblWeapon.D
                FROM TblModel
                INNER JOIN TblInGame ON TblModel.ModelID = TblInGame.ModelID
                INNER JOIN TblWeapon ON TblWeapon.WeaponID = TblInGame.WeaponID
                WHERE TblModel.ModelID = ?''', (ModelIDlist))
        wrow = cursor.fetchall()
        for x in wrow:
            if x[2] == "R":
                self.Rweapon = weapon(self, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
            else:
                self.Mweapon = weapon(self, x[0], x[1], "M", self.A, 1, self.S + x[5], x[6], x[7])
        if self.Mweapon == None:
            self.Mweapon = weapon(self, "DEFAULT", "MELEE", "M", self.A, 1, self.S, 0, 1)
        self.mrGroup.add(rangecircle(surface, self, self.Mweapon))
        if self.Rweapon is not None:
            self.rGroup.add(rangecircle(surface, self, self.Rweapon))

    def modelmove(self, modelcount, cGroup):
        if len(self.mGroup.sprites()) == 0:
            self.mGroup.add(movementcircle(self.surface, self, self.M))
        self.mGroup.state = True
        moved = False
        while not moved:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    lastpos = self.rect.center
                    self.rect.center = event.pos
                    if pygame.sprite.collide_circle(self, self.mGroup.sprites()[0]) and modelcount == 0:
                        cGroup.update()
                        draw()
                        self.mGroup.state = False
                        draw()
                        moved = True

                    elif pygame.sprite.collide_circle(self, self.mGroup.sprites()[
                        0]) and modelcount > 0 and self.coherencycheck(cGroup):
                        cGroup.update()
                        draw()
                        self.mGroup.state = False
                        draw()
                        moved = True

                    elif not pygame.sprite.collide_circle(self, self.mGroup.sprites()[
                        0]) and not pygame.sprite.collide_circle(self, self.mGroup.sprites()[0]):
                        print("That is not a valid move.")
                        self.rect.center = lastpos
                        draw()

                if event.type == pygame.QUIT:
                    print("Saving ...")
                    pygame.quit()
                    quit()

            draw()
            clock.tick(30)
        draw()
        return moved

    def coherencycheck(self, cGroup):
        flag = False
        cGroup.update()
        if len(pygame.sprite.spritecollide(self, cGroup, False)) > 1:
            flag = True
            return flag
        else:
            flag = False
            return flag

    def modeldeploy(self, modelcount, cGroup, dGroup):
        self.mGroup.state = True
        moved = False
        while not moved:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    lastpos = self.rect.center
                    self.rect.center = event.pos
                    if pygame.sprite.spritecollide(self, dGroup, False) and modelcount == 0:
                        cGroup.update()
                        draw()
                        self.mGroup.state = False
                        draw()
                        moved = True

                    elif pygame.sprite.spritecollide(self, dGroup, False) and modelcount > 0 and self.coherencycheck(
                            cGroup):
                        cGroup.update()
                        draw()
                        self.mGroup.state = False
                        draw()
                        moved = True

                    elif not pygame.sprite.spritecollide(self, dGroup, False):
                        print("That is not a valid move.")
                        self.rect.center = lastpos
                        draw()
                        self.mGroup.state = False
                        draw()

                if event.type == pygame.QUIT:
                    print("Saving ...")
                    pygame.quit()
                    quit()

            draw()
            clock.tick(30)
        draw()
        return moved

    def modelclickcheck(self, clickpos):
        if self.rect.collidepoint(clickpos):
            return True
        else:
            return False


class deployzone(pygame.sprite.Sprite):
    def __init__(self, surface, team):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.black = [0, 0, 0]
        self.color = [255, 87, 45]
        self.incolor = [255, 89, 0]
        if team[0] == 1:
            self.pos = (0, 0)
        else:
            self.pos = (600, 0)
        self.image = pygame.Surface((120, 480))
        self.image.set_alpha(100)
        self.image.set_colorkey(self.black)
        self.image.fill(self.color, rect=None, special_flags=0)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


class movementcircle(pygame.sprite.Sprite):
    def __init__(self, surface, model, distance):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.model = model
        self.radius = (distance * 10) + int(self.model.radius)
        self.pos = (self.radius, self.radius)
        self.color = [0, 253, 12]
        self.incolor = [174, 255, 168]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(60)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius), 3)
        self.rect = self.image.get_rect()
        self.rect.center = model.rect.center

    def update(self):
        self.rect.center = self.model.rect.center


class movementgroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.state = False


class coherencycircle(pygame.sprite.Sprite):
    def __init__(self, surface, model):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.model = model
        self.radius = int(self.model.radius) + 20
        self.pos = (self.radius), (self.radius)
        self.color = [0, 225, 255]
        self.incolor = [142, 241, 255]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(60)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (model.rect.center)

    def update(self):
        self.rect.center = self.model.rect.center


class coherencygroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)


class rangecircle(pygame.sprite.Sprite):
    def __init__(self, surface, model, weapon):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.model = model
        self.radius = (weapon.Range * 10) + int(self.model.radius)
        self.pos = (self.radius, self.radius)
        self.color = [255, 0, 0]
        self.incolor = [255, 119, 45]
        self.black = [0, 0, 0]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(self.black)
        self.image.set_alpha(30)
        pygame.draw.circle(self.image, self.incolor, self.pos, (self.radius), 0)
        pygame.draw.circle(self.image, self.color, self.pos, (self.radius), 3)
        self.rect = self.image.get_rect()
        self.rect.center = model.rect.center

    def update(self):
        self.rect.center = self.model.rect.center


class rangegroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.state = False


class fight():
    def __init__(self, fightlist, unit1, unit2):
        self.fighterlist = [unit1, unit2]
        unit1.infight = True
        unit2.infight = True
        unit1.fightin = self
        unit2.fightin = self
        print("Player", unit1.team, "'s", unit1.sprites()[0].Modelname,
              "unit is now in combat with Player", unit2.team, "'s",
              unit2.sprites()[0].Modelname, "unit.")
        self.state = True

    def check(self, fightlist):
        for unit in self.fighterlist:
            if not unit.sprites():
                self.fighterlist.remove(unit)
        if not self.fighterlist:
            fightlist.remove(self)
        elif len(self.fighterlist) == 1:
            self.fighterlist[0].infight = False
            fightlist.remove(self)
        else:
            if self.fighterlist[0].fought and self.fighterlist[1].fought:
                self.state = False

    def resolve(self, controllingplayer):
        if self.fighterlist[0].chargebuff or self.fighterlist[0].team == controllingplayer.team:
            attacker = self.fighterlist[0]
            target = self.fighterlist[1]
        else:
            attacker = self.fighterlist[1]
            target = self.fighterlist[0]
        print("Resolving", attacker.sprites()[0].Modelname, "vs",
              target.sprites()[0].Modelname, "fight")
        attacks = attacker.sprites()[0].A * len(attacker.sprites())
        attacker.unitfight(target, attacks)
        attacker.fought = True
        attacker.chargebuff = False


class unit(pygame.sprite.Group):
    def __init__(self, surface, id, team, size):
        pygame.sprite.Group.__init__(self)
        self.surface = surface
        self.id = id
        self.idlist = [id]
        self.team = team
        self.size = size
        self.deadlist = []
        self.shot = False
        self.fought = False
        self.charged = False
        self.chargebuff = False
        self.infight = False
        self.fightin = None
        self.cGroup = coherencygroup()
        self.chGroup = chargegroup()

    def unitmove(self):
        modelcount = 0
        if not self.infight:
            print("Now moving your:", self.sprites()[0].Modelname, "unit")
            for model in self.sprites():
                self.cGroup.add(coherencycircle(self.surface, model))
                if model.modelmove(modelcount, self.cGroup) == True:
                    modelcount = modelcount + 1
                    model.mGroup.update()
        else:
            print("Your", self.sprites()[0].Modelname, "unit is locked in combat!")
        self.cGroup.empty()

    def createmodels(self):
        cursor.execute('''
        SELECT TblInGame.ModelID FROM TblInGame
        WHERE TblInGame.UnitID = ?''', self.idlist)
        row = cursor.fetchall()
        for i in range(0, self.size):
            for x in row:
                self.add(model(self.surface, x[0]))

    def unitdeploy(self, dGroup):
        modelcount = 0
        print("Now deploying your:", self.sprites()[0].Modelname, "unit")
        for model in self.sprites():
            self.cGroup.add(coherencycircle(self.surface, model))
            if model.modeldeploy(modelcount, self.cGroup, dGroup) == True:
                modelcount = modelcount + 1
                model.mGroup.update()
                model.rGroup.update()
        self.cGroup.empty()

    def unitshoot(self, target, shots):
        hits = 0
        attacker = self.sprites()[0]
        print("Player", self.team, "'s", attacker.Modelname, "unit is attacking Player", target.team, "'s",
              target.sprites()[0].Modelname, "unit.")
        print("Roll to hit:", attacker.BS)
        for shot in range(0, shots):
            roll = random.randint(1, 6)
            if roll >= attacker.BS:
                hits = hits + 1
        print("Number of hits:", hits)
        wound("R", self, target, hits, False)

    def unitfight(self, target, attacks):
        hits = 0
        attacker = self.sprites()[0]
        print("Player", self.team, "'s", attacker.Modelname, "unit is attacking Player", target.team, "'s",
              target.sprites()[0].Modelname, "unit in close combat!")
        print("Roll to hit:", attacker.BS)
        for attack in range(0, attacks):
            roll = random.randint(1, 6)
            if roll >= attacker.WS:
                hits = hits + 1
        print("Number of hits:", hits)
        wound("M", self, target, hits, False)

    def unitclickcheckshoot(self, clickpos, attackplayer):
        print("Checking", self.sprites()[0].Modelname, "unit")
        if self.sprites()[0].Rweapon == None and self.team == attackplayer.team[0]:
            print("This unit is Melee only")
        elif self.shot:
            print("This unit has already shot this turn.")
        elif self.infight:
            print("This unit is locked in combat!")
        elif not self.sprites():
            print("This unit has been slain")
        else:
            for model in self.sprites():
                if model.modelclickcheck(clickpos) and not self.shot:
                    return self
                else:
                    pass

    def unitclickcheckcharge(self, clickpos, attackplayer):
        print("Checking", self.sprites()[0].Modelname, "unit")
        if self.charged:
            print("This unit has already charged this turn")
        elif not self.sprites():
            print("This unit has been slain")
        else:
            for model in self.sprites():
                if model.modelclickcheck(clickpos) and not self.charged:
                    return self
                else:
                    pass

    def unitclickcheckfight(self, clickpos, controllingplayer):
        print("Checking", self.sprites()[0].Modelname, "unit")
        if self.fought and self.team == controllingplayer.team[0]:
            print("This unit has already fought this turn")
        elif not self.sprites():
            print("This unit has been slain")
        else:
            for model in self.sprites():
                if model.modelclickcheck(clickpos):
                    return self
                else:
                    pass

    def switchstateR(self, value):
        for model in self.sprites():
            model.rGroup.state = value

    def switchstateCh(self, value):
        for model in self.sprites():
            model.chGroup.state = value

    def switchstateMr(self, value):
        for model in self.sprites():
            model.mrGroup.state = value

    def update(self):
        for model in self.sprites():
            model.rGroup.update()
            model.mrGroup.update()
            model.mGroup.update()
            model.chGroup.update()


def create_connection(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return cursor


class player:
    def __init__(self, surface, playerID, team):
        self.surface = surface
        self.playerID = playerID
        self.team = [team]
        self.units = []
        self.VP = 0
        self.moved = False
        self.psyked = False
        self.shot = False
        self.charged = False
        self.fought = False
        self.deadlist = []

        if team == 1:
            self.side = "l"
        else:
            self.side = "r"
        self.dGroup = pygame.sprite.Group()

    def deploy(self):
        self.dGroup.add(deployzone(self.surface, self.team))
        for unit in self.units:
            unit.unitdeploy(self.dGroup)

    def createunits(self):
        cursor.execute('''
        SELECT TblInGame.UnitID, TblInGame.Team, TblInGame.UnitSize FROM TblInGame
        WHERE TblInGame.Team = ?''', self.team)
        row = cursor.fetchall()
        for x in row:
            self.units.append(unit(self.surface, x[0], x[1], x[2]))
        for i in range(0, len(self.units)):
            self.units[i].createmodels()

    def drawU(self):
        for unit in self.units:
            unit.draw(board)

    def clearU(self):
        for unit in self.units:
            unit.clear(board, back)

    def drawM(self):
        for unit in self.units:
            for model in unit.sprites():
                if model.mGroup.state == True:
                    model.mGroup.draw(board)

    def clearM(self):
        for unit in self.units:
            for model in unit.sprites():
                model.mGroup.clear(board, back)

    def drawR(self):
        for unit in self.units:
            for model in unit.sprites():
                if model.rGroup.state == True:
                    model.rGroup.draw(board)

    def clearR(self):
        for unit in self.units:
            for model in unit.sprites():
                model.rGroup.clear(board, back)

    def drawC(self):
        for unit in self.units:
            unit.cGroup.draw(board)

    def clearC(self):
        for unit in self.units:
            unit.cGroup.clear(board, back)

    def drawD(self):
        self.dGroup.draw(board)

    def clearD(self):
        self.dGroup.clear(board, back)

    def drawCh(self):
        for unit in self.units:
            for model in unit.sprites():
                if model.chGroup.state == True:
                    model.chGroup.draw(board)

    def clearCh(self):
        for unit in self.units:
            for model in unit.sprites():
                model.chGroup.clear(board, back)

    def drawMr(self):
        for unit in self.units:
            for model in unit.sprites():
                if model.mrGroup.state == True:
                    model.mrGroup.draw(board)

    def clearMr(self):
        for unit in self.units:
            for model in unit.sprites():
                model.mrGroup.clear(board, back)

    def resetswitches(self):
        for unit in self.units:
            unit.shot = False
            unit.charged = False
            unit.fought = False

    def rangeswitch(self, value):
        for unit in self.units:
            unit.switchstateR(value)

    def chargeswitch(self, value):
        for unit in self.units:
            unit.switchstateCh(value)

    def mrswitch(self, value):
        for unit in self.units:
            unit.switchstateMr(value)

    def deadcheck(self):
        for i in range(0, len(self.units) - 1):
            if not self.units[i]:
                self.deadlist.append(self.units.pop(i))


def shootphase(currentplayer):
    if currentplayer == playerlist[0]:
        otherplayer = playerlist[1]
    else:
        otherplayer = playerlist[0]
    attackselected = False
    targetselected = False
    shooting = True
    while shooting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shooting = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clickpos = event.pos
                if not attackselected and not targetselected:
                    attacker, catch = shootcheck(clickpos, currentplayer, currentplayer, None, False)
                    if attacker == None:
                        break
                    print(attacker.sprites()[0].Modelname, "unit is shooting")
                    attacker.update()
                    attacker.switchstateR(True)
                    attackselected = True
                elif attackselected and not targetselected:
                    target, shots = shootcheck(clickpos, otherplayer, currentplayer, attacker, True)
                    if target == None:
                        break
                    print("Target is", target.sprites()[0].Modelname, "unit.")
                    print("Number of shots:", shots)
                    targetselected = True

            if attackselected and targetselected:
                attacker.unitshoot(target, shots)
                attackselected = False
                targetselected = False
                attacker.shot = True
                attacker.switchstateR(False)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                currentplayer.rangeswitch(False)
                attackselected = False
                targetselected = False
                print("Selection reset.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    currentplayer.shot = True
                    currentplayer.rangeswitch(False)
                    print("Ending shooting phase.")
                    shooting = False

            clock.tick(30)
            draw()


def chargephase(currentplayer):
    if currentplayer == playerlist[0]:
        otherplayer = playerlist[1]
    else:
        otherplayer = playerlist[0]
    chargeselected = False
    targetselected = False
    charging = True
    while charging:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                charging = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clickpos = event.pos
                if not chargeselected and not targetselected:
                    chargeunit = chargecheck(clickpos, currentplayer, None, False)
                    if chargeunit == None:
                        break
                    print("Charging unit is", chargeunit.sprites()[0].Modelname, "unit")
                    print("Please select target unit")
                    for model in chargeunit.sprites():
                        model.chGroup.update()
                    chargeunit.switchstateCh(True)
                    chargeselected = True
                elif chargeselected and not targetselected:
                    target = chargecheck(clickpos, otherplayer, chargeunit, True)
                    if target == None:
                        break
                    print("Target is", target.sprites()[0].Modelname, "unit.")
                    targetselected = True

            if chargeselected and targetselected:
                chargeselected = False
                targetselected = False
                chargeunit.charged = True
                chargeunit.chargebuff = True
                if target.sprites()[0].Rweapon == None:
                    print("This unit is melee only, and cannot fire overwatch.")
                else:
                    print("Firing overwatch!")
                    overwatch(chargeunit, target)
                chargepass, moveinch = chargetest(chargeunit, target)
                if chargepass:
                    chargemove(chargeunit, target, moveinch)
                    fightlist.append(fight(fightlist, chargeunit, target))

                    chargeunit.switchstateCh(False)
                    pass
                else:
                    chargeunit.switchstateCh(False)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                currentplayer.chargeswitch(False)
                chargeselected = False
                targetselected = False
                print("Selection reset.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    currentplayer.charged = True
                    currentplayer.chargeswitch(False)
                    print("Ending charge phase.")
                    charging = False

            clock.tick(30)
            draw()


def fightphase(currentplayer):
    originalplayer = currentplayer
    if currentplayer == playerlist[0]:
        otherplayer = playerlist[1]
    else:
        otherplayer = playerlist[0]
    attackselected = False
    targetselected = False
    fighting = True
    while fighting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fighting = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clickpos = event.pos
                if not attackselected and not targetselected:
                    attacker = fightcheck(clickpos, currentplayer, currentplayer, None, False)
                    if attacker == None:
                        break
                    print(attacker.sprites()[0].Modelname, "unit is attacking")
                    attacker.update()
                    attacker.switchstateMr(True)
                    attackselected = True
                elif attackselected and not targetselected:
                    target = fightcheck(clickpos, otherplayer, currentplayer, attacker, True)
                    if target == None:
                        break
                    if target.chargebuff:
                        print("Units that charged must attack first")
                        break
                    print("Target is", target.sprites()[0].Modelname, "unit.")
                    targetselected = True

            if attackselected and targetselected:
                selectedfight = commonfight(attacker, target)
                if selectedfight is not None:
                    selectedfight.resolve(currentplayer)
                    selectedfight.check(fightlist)
                    attacker.fought = True
                    currentplayer, otherplayer = otherplayer, currentplayer
                    print("Player", currentplayer.team[0], "will now resolve a combat")
                targetselected = False
                attackselected = False
                currentplayer.mrswitch(False)
                otherplayer.mrswitch(False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    targetselected = False
                    attackselected = False
                    currentplayer.mrswitch(False)
                    otherplayer.mrswitch(False)
                    currentplayer, otherplayer = otherplayer, currentplayer
                    print("Player", currentplayer.team[0], "will now resolve a combat")

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                currentplayer.mrswitch(False)
                attackselected = False
                targetselected = False
                print("Selection reset.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    originalplayer.fought = True
                    currentplayer.mrswitch(False)
                    otherplayer.mrswitch(False)
                    print("Ending fight phase.")
                    fighting = False

            clock.tick(30)
            draw()


def commonfight(unit1, unit2):
    selectedfight = None
    for fight in fightlist:
        if unit1 in fight.fighterlist and unit2 in fight.fighterlist:
            selectedfight = fight
    if selectedfight == None:
        print("These two units are not in combat together.")
    else:
        return selectedfight


def informationphase():
    print("Information phase started")


def chargemove(chargeunit, target, moveinch):
    tempM = chargeunit.sprites()[0].M
    moved = False
    while not moved:
        for model in chargeunit.sprites():
            model.M = moveinch
            model.temp = model.rect.center
        chargeunit.unitmove()
        if closestpair(chargeunit, target) <= 10 + chargeunit.sprites()[0].radius + target.sprites()[0].radius:
            moved = True
        else:
            print('Please move at least 1 charging model within 1" of at least 1 target model.')
            for model in chargeunit.sprites():
                model.rect.center = model.temp
                model.M = tempM
                model.mGroup.update()
    for model in chargeunit.sprites():
        model.M = tempM


def chargetest(chargeunit, target):
    mindist = closestpair(chargeunit, target) - target.sprites()[0].radius
    print("Charge roll needed:", int(mindist / 10))
    moveinch = random.randint(1, 6) + random.randint(1, 6)
    print("You rolled", moveinch, "for charge distance.")
    chargedist = (((moveinch) * 10) + chargeunit.sprites()[0].radius)
    if chargedist >= mindist:
        print("Charge successful")
        return True, moveinch
    else:
        print("Charge failed")
        return False, moveinch


def overwatch(chargeunit, target):
    temp = 0
    for model in target.sprites():
        temp = model.BS
        model.BS = 6
    target.unitshoot(chargeunit, len(target.sprites()))
    for model in target.sprites():
        model.BS = temp


def chargecheck(clickpos, player, chargeunit, selectingtarget):
    inrange = False
    selectedlist = []
    for unit in player.units:
        selectedunit = unit.unitclickcheckcharge(clickpos, player)
        if selectedunit != None:
            selectedlist.append(selectedunit)
            if selectingtarget:
                chargeunit.switchstateCh(True)
                for model in chargeunit.sprites():
                    if pygame.sprite.spritecollide(model.chGroup.sprites()[0], selectedunit, False,
                                                   pygame.sprite.collide_circle):
                        inrange = True
                if not inrange:
                    print("This target is not in range, please select again")
                    return None
        elif len(selectedlist) > 1:
            print("Please select only 1 unit")
            return None

    try:
        return selectedlist[0]
    except IndexError:
        print("No unit selected")
        return None


def shootcheck(clickpos, player, attackplayer, attacker, selectingtarget):
    inrange = False
    selectedlist = []
    shots = 0
    for unit in player.units:
        selectedunit = unit.unitclickcheckshoot(clickpos, attackplayer)
        if selectedunit != None:
            selectedlist.append(selectedunit)
            if selectingtarget:
                attacker.switchstateR(True)
                shotsperwep = getshots(attacker)
                for model in attacker.sprites():
                    if pygame.sprite.spritecollide(model.rGroup.sprites()[0], selectedunit, False,
                                                   pygame.sprite.collide_circle):
                        inrange = True
                        shots = shots + shotsperwep
                if not inrange:
                    print("Target is not in range, please select again")
                    return None, 0
        elif len(selectedlist) > 1:
            print("Please select only 1 unit")
            return None, 0

    try:
        return selectedlist[0], shots
    except IndexError:
        print("No unit selected")
        return None, 0


def getshots(unit):
    shots = 0
    shotsholder = unit.sprites()[0].Rweapon.Shots
    if shotsholder == "D6":
        shots = random.randint(1, 6)
    elif shotsholder == "D3":
        shots = random.randint(1, 3)
    else:
        shots = int(shotsholder)
    return shots


def fightcheck(clickpos, playertocheck, controllingplayer, attacker, selectingtarget):
    selectedlist = []
    for unit in playertocheck.units:
        selectedunit = unit.unitclickcheckfight(clickpos, controllingplayer)
        if selectedunit is not None:
            selectedlist.append(selectedunit)
            if selectingtarget:
                attacker.switchstateMr(True)
        elif len(selectedlist) > 1:
            print("Please select only one unit")
            return None
    try:
        return selectedlist[0]
    except IndexError:
        print("No unit selected")
        return None


def wound(RorM, attackunit, targetunit, hits, mortal):
    attacker = attackunit.sprites()[0]
    target = targetunit.sprites()[0]
    wounds = 0
    damage = 0
    # choose weapon
    if RorM == "R":
        weapon = attacker.Rweapon
    elif RorM == "M":
        weapon = attacker.Mweapon
    # get roll
    if weapon.S >= target.T * 2:
        rollneeded = 2
    elif weapon.S * 2 <= target.T:
        rollneeded = 6
    elif weapon.S > target.T:
        rollneeded = 3
    elif weapon.S == target.T:
        rollneeded = 4
    elif weapon.S < target.T:
        rollneeded = 5
    # roll for wounds
    for hit in range(0, hits):
        roll = random.randint(1, 6)
        if roll >= rollneeded:
            wounds = wounds + 1
    print("Scored", wounds, "wounds")
    # calculate damage
    print("Weapon damage:", weapon.D)
    if weapon.D == "D6":
        damage = random.randint(1, 6)
    elif weapon.D == "D3":
        damage = random.randint(1, 3)
    else:
        damage = int(weapon.D)
    print("Inflicting", damage, "D per wound")
    # getting save
    if target.ISv != "":
        Isave = target.ISv
    print("Armour save:", target.Sv)
    print("Weapon AP:", weapon.AP)
    save = target.Sv - weapon.AP
    print("Armour save after AP:", save)
    if Isave >= 2 and Isave <= save:
        save = Isave
        print("Using invulnerable save!")
    print("Saving roll is", save)
    # apply damage
    for model in targetunit.sprites():
        while model.alive() and wounds > 0:
            if random.randint(1, 6) >= save:
                print("Saved!")
                wounds = wounds - 1
            else:
                print("Wound!")
                model.W = model.W - damage
                print("Remaining wounds:", model.W)
                wounds = wounds - 1
            if model.W <= 0:
                targetunit.deadlist.append(model)
                model.kill()
                print("Your", model.Modelname, "has been slain!")
    player1.deadcheck()
    player2.deadcheck()


def nextturn(playerlist, currentplayer):
    currentplayer.moved = False
    currentplayer.psyked = False
    currentplayer.shot = False
    currentplayer.charged = False
    currentplayer.fought = False
    for player in playerlist:
        player.resetswitches()
    if currentplayer == playerlist[0]:
        currentplayer = playerlist[1]
    else:
        currentplayer = playerlist[0]
    print("It is now Player", currentplayer.team[0], "'s turn")
    return currentplayer


def closestpair(unit1, unit2):
    mindist = float("inf")
    for model1 in unit1.sprites():
        for model2 in unit2.sprites():
            tempdist = dist(model1, model2)
            if tempdist < mindist:
                mindist = tempdist
    return mindist


def dist(model1, model2):
    x1 = model1.rect.centerx
    x2 = model2.rect.centerx
    y1 = model1.rect.centery
    y2 = model2.rect.centery
    dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


def draw():
    # clear first
    player1.clearU()
    player1.clearC()
    player1.clearM()
    player1.clearD()
    player1.clearR()
    player1.clearCh()
    player1.clearMr()
    player2.clearU()
    player2.clearC()
    player2.clearM()
    player2.clearD()
    player2.clearR()
    player2.clearCh()
    player2.clearMr()
    TerrainGroup.clear(board, back)
    # draw in order, lowest first
    TerrainGroup.draw(board)
    player1.drawR()
    player2.drawR()
    player1.drawCh()
    player2.drawCh()
    player1.drawMr()
    player2.drawMr()
    player1.drawD()
    player2.drawD()
    player1.drawM()
    player2.drawM()
    player1.drawC()
    player2.drawC()
    player1.drawU()
    player2.drawU()
    pygame.display.update()


def gameloop():
    gameon = True
    deployed = False

    currentplayer = pickplayer(playerlist)[0]
    print("Player", currentplayer.team[0], "will choose who is deploying first.")
    valid = False
    while not valid:
        choice = input("Please type 1 if you wish to deploy first, and 2 if you wish to deploy second. ")
        if choice == "1":
            print("Player", currentplayer.team[0], "will deploy first. GL HF!")
            valid = True
        elif choice == "2":
            currentplayer = playerlist[1]
            playerlist[0], playerlist[1] = playerlist[1], playerlist[0]
            print("Player", currentplayer.team[0], "will deploy first. GL HF!")
            valid = True
        else:
            print("Input not recognised, please try again.")
    deploy(playerlist)
    deployed = True
    print("Player", currentplayer.team[0], "will choose who gets the first turn.")
    valid = False
    while not valid:
        choice = input("Please type 1 if you wish to have the first turn, and 2 if you wish to have the second turn. ")
        if choice == "1":
            print("Player", currentplayer.team[0], "will have the first turn. GL HF!")
            valid = True
        elif choice == "2":
            currentplayer = playerlist[1]
            playerlist[0], playerlist[1] = playerlist[1], playerlist[0]
            print("Player", currentplayer.team[0], "will have the first turn. GL HF!")
            valid = True

    print("Player", playerlist[1].team[0],
          "can Seize The Initiative on  D6 roll of 6. Do you wish to Seize The Initiative?")
    valid = False
    while not valid:
        seizechoice = input("(y/n) ")
        if seizechoice == "y":
            roll = random.randint(1, 6)
            print("You rolled:", roll)
            if roll == 6:
                print("Congratulations! Player", playerlist[1].team[0],
                      ", you have successfully Seized The Initiative!")
                currentplayer = playerlist[1]
                playerlist[0], playerlist[1] = playerlist[1], playerlist[0]
            else:
                print("Too bad! Player", playerlist[1].team[0],
                      ", you have failed to Seized The Initiative.")
            valid = True
        elif seizechoice == "n":
            valid = True
        else:
            valid = False

    deployed = True

    print("It is player", currentplayer.team[0], "'s turn")
    while gameon:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameon = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and not currentplayer.moved and not currentplayer.shot and not currentplayer.charged and deployed:
                    print("Player", currentplayer.team[0], "'s Move phase begun")
                    movephase(currentplayer)
                    currentplayer.moved = True

                if event.key == pygame.K_n:
                    currentplayer = nextturn(playerlist, currentplayer)

                if event.key == pygame.K_s and not currentplayer.shot and currentplayer.moved and deployed:
                    print("Starting Player", currentplayer.team[0], "'s shooting phase")
                    shootphase(currentplayer)

                if event.key == pygame.K_c and not currentplayer.charged and currentplayer.shot and currentplayer.moved and deployed:
                    print("Starting Player", currentplayer.team[0], "'s charge phase")
                    chargephase(currentplayer)

                if event.key == pygame.K_f and currentplayer.charged and currentplayer.shot and currentplayer.moved and deployed:
                    print("Starting Player", currentplayer.team[0], "'s fight phase")
                    fightphase(currentplayer)

                if event.key == pygame.K_i:
                    pass  # info phase

        clock.tick(30)
        draw()

    # do saving stuff
    pygame.quit()
    quit()


print("Welcome to the Warhammer: 40,000 board game")
print("Please wait whilst the game is initialised")
print("If you are unfamiliar with the controls of this game, check the readme.txt")
conn = sqlite3.connect("res/data/BackEndDB.db")
cursor = conn.cursor()

back = pygame.image.load("res/back/boardbackdesert.png")

TerrainDict = {"bunker1": "res/terrain/1bunker_1x1.png",
               "bunker2": "res/terrain/2bunker_1x2.png",
               "bunker3": "res/terrain/3bunker_2x1.png",
               "bunker4": "res/terrain/4bunker_round_2x1.png",
               "bunker5": "res/terrain/5bunker_round_2x1.png",
               "bunker6": "res/terrain/6bunker_round.png",
               "bunker7": "res/terrain/7bunker_round.png",
               "bunker8": "res/terrain/8bunker_big.png"}

BaseDict = {"WARRIO": "res/model/WarriorBase.png",
            "OVERLO": "res/model/OverlordBase.png",
            "DESLOR": "res/model/DestroyerLordBase.png",
            "CRYPTE": "res/model/CryptekBase.png"}

turn = 0

pygame.init()

display_width = 720
display_height = 480
white = [255, 255, 255]
black = [0, 0, 0]

board = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Warhammer: 40,000 board game")
clock = pygame.time.Clock()

board.fill(white)
back = pygame.image.load("res/back/boardbackdesert.png")
icon = pygame.image.load("res/window/icon.png")
pygame.display.set_icon(icon)

board.blit(back, (0, 0))

TerrainGroup = TerrainGroup(board)
TerrainGroup.createterrain()

player1 = player(board, 1, 1)
player2 = player(board, 2, 2)
playerlist = [player1, player2]

fightlist = []

player1.createunits()
player2.createunits()

if __name__ == "__main__":
    gameloop()
