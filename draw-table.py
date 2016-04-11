#basic display graphics, draw table with pockets and balls given a list of ball objects
import pygame
import math

screen = pygame.display.set_mode((1579,873))

table = pygame.image.load('pool_table.png')

holes = ((83,78),(790,57),(1499,80),(83,791),(790,810),(1499,790))

running = True
while running:
	screen.blit(table,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	pygame.display.update()