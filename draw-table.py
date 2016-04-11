#basic display graphics, draw table with pockets and balls given a list of ball objects
import pygame
import math

class Table(object):
	def __init__(self, pockets ,top = 84,bottom = 789,left = 84,right =1494, ball_list):
		self.pockets = ((83,78),(790,57),(1499,80),(83,791),(790,810),(1499,790))
		self.walls = [top, bottom, left, right]
		self.ball_list = ball_list

screen = pygame.display.set_mode((1579,873))

table = pygame.image.load('pool_table.png')

def draw_table():
	running = True
	while running:
		screen.blit(table,(0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		pygame.display.update()