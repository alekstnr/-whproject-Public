import pygame
import random

#loading images
def TerrainLoad():
    bunker1 = pygame.image.load("1bunker_1x1.png")
    bunker2 = pygame.image.load("2bunker_1x2.png")
    bunker3 = pygame.image.load("3bunker_2x1.png")
    bunker4 = pygame.image.load("4bunker_round_2x1.png")
    bunker5 = pygame.image.load("5bunker_round_2x1.png")
    bunker6 = pygame.image.load("6bunker_round.png")
    bunker7 = pygame.image.load("7bunker_round.png")
    bunker8 = pygame.image.load("8bunker_big.png")
    TerrainList = [bunker1, bunker2, bunker3, bunker4, bunker5, bunker6, bunker7, bunker8]
    return TerrainList

def BoardInit(TerrainList, Surface):
    TerrainNo = random.randint(3,5)
    random.shuffle(TerrainList)
    for i in range(0, TerrainNo):
        TerrainList[i] = pygame.transform.rotate(TerrainList[i], random.randint(0, 360))
        Surface.blit(TerrainList[i], (random.randint(100, 620), random.randint(60, 420)))

