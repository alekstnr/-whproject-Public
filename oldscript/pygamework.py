import pygame
import sys

display_width = 720
display_height = 480

pygame.init()
board = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Warhammer: 40,000 board game")
board.fill((255,255,255))
pygame.draw.line(board, (0, 0, 0), (0, 239), (720, 239), 2)
pygame.draw.line(board, (0, 0, 0), (239, 0), (239, 480), 2)
pygame.draw.line(board, (0, 0, 0), (479, 0), (479, 480), 2)

clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    clock.tick(10)
