#will take in list of ball objects and current cue position/direction, output end state of balls
#later will output lines for projected ball motions
import pygame
import numpy as np
import ball
import math

class line(object):
	# draw lines
	def __init__(self, table, start, end, width = 1, color = pygame.Color('white')):
		self.width = width
		self.color = color
		self.table = table
		self.start = start
		self.end = end
	def draw(self):
		pygame.draw.line(self.table, 
						 self.color,
						 self.start,
						 self.end,
						 self.width)

class ball_collision:
	# Given two colliding balls, output their states after collision
	
	def __init__(self, ball_1, ball_2):
		self.ball_1 = ball_1
		self.ball_2 = ball_2
	
	def after_collision(self):
		# Calculate velocity after collision between two balls
		m1 = self.ball_1.mass
		m2 = self.ball_2.mass
		pos_1 = np.array(self.ball_1.pos)
		pos_2 = np.array(self.ball_2.pos)
		vel_1 = np.array(self.ball_1.vel)
		vel_2 = np.array(self.ball_2.vel)

		n = pos_2 - pos_1
		un = n / math.sqrt(np.vdot(n,n))
		ut = np.array(-un[1],un[0])

		vel_1n = np.vdot(un, vel_1)
		vel_1t = np.vdot(ut, vel_1)
		vel_2n = np.vdot(un, vel_2)
		vel_2t = np.vdot(ut, vel_2)

		new_vel_1t = vel_1t * ut
		new_vel_2t = vel_2t * ut
		new_vel_1n = (vel_1n*(m1-m2) + 2*m2*vel_2n)/(m1+m2) * un
		new_vel_2n = (vel_2n*(m2-m1) + 2*m1*vel_1n)/(m1+m2) * un

		new_vel_1 = new_vel_1n + new_vel_1t
		new_vel_2 = new_vel_2n + new_vel_2t

		self.ball_1.vel = list(new_vel_1)
		self.ball_2.vel = list(new_vel_2)

	def update(self):
		# Update ball position
		self.ball_1.pos += self.ball_1.vel
		self.ball_2.pos += self.ball_2.vel


class cue_hit:
	
	def __init__(self, cue, cueball):
		self.cue = cue
		self.ball = cueball
	
	def check_hit(self):
		# check if the cue will hit the cue ball
		pass
	def hit(self):
		# return velocity of the cue ball after hit 
		pass
		
if __name__ == '__main__':
	main()















