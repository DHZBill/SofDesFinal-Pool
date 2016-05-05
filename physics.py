import numpy as np
import math
from ball import ball

def update(ball1):
	'''Updates the position of the ball using a time step, and decreases the velocity of the ball with each step'''
	# include friction
	step = 0.2
	slow = 1
	if ball1.velMagnitude != 0:
		ball1.pos = [ball1.pos[0] + ball1.vel[0] * ball1.velMagnitude * step, ball1.pos[1] + ball1.vel[1] * ball1.velMagnitude * step]
	ball1.velMagnitude -= slow
	if(ball1.velMagnitude < 0):
		ball1.velMagnitude = 0
	return ball1

def ball_collision(ball_1, ball_2): 
	'''Calculates the end velocity of two balls after a collision'''
	m1 = ball_1.mass
	m2 = ball_2.mass
	# transform position and velocity into vectors.
	pos_1 = np.array(ball_1.pos)
	pos_2 = np.array(ball_2.pos)
	vel_1 = np.array([ball_1.vel[0] * ball_1.velMagnitude, ball_1.vel[1] * ball_1.velMagnitude])
	vel_2 = np.array([ball_2.vel[0] * ball_2.velMagnitude, ball_2.vel[1] * ball_2.velMagnitude])
	# calculate the distance between 2 balls in vector, and get its direction.
	n = pos_2 - pos_1
	thing = int(math.sqrt(np.dot(n,n)))
	if thing == 0:
		return [ball_1.vel, ball_2.vel, ball_1.pos, ball_2.pos]
	un = n / thing
	ut = np.array(-un[1],un[0])
	# calculate the magnitude of velocity on each direction 
	vel_1n = np.dot(un, vel_1) # use numpy's dot, not vdot
	vel_1t = np.dot(ut, vel_1)
	vel_2n = np.dot(un, vel_2)
	vel_2t = np.dot(ut, vel_2)
	# calculate the new velocity for each ball
	new_vel_1t = vel_1t * ut
	new_vel_2t = vel_2t * ut
	new_vel_1n = (vel_1n*(m1-m2) + 2*m2*vel_2n)/(m1+m2) * un
	new_vel_2n = (vel_2n*(m2-m1) + 2*m1*vel_1n)/(m1+m2) * un

	new_vel_1 = new_vel_1n + new_vel_1t
	new_vel_2 = new_vel_2n + new_vel_2t
	# separate two balls after collision. Ensure that there is no overlap after collision.
	dist = math.sqrt(np.dot(pos_1 - pos_2, pos_1 - pos_2))

	while dist <= (ball_1.radius + ball_2.radius):
		pos_1 += new_vel_1 * 0.1
		pos_2 += new_vel_2 * 0.1
		dist = math.sqrt(np.dot(pos_1 - pos_2, pos_1 - pos_2))

	# return position and velocity after collision
	return [list(new_vel_1), list(new_vel_2), pos_1, pos_2]

		
def run(ballList, walls, pockets):
	'''Iterates over all balls in a list to check for pocketed balls, wall collisions, and collisions with other balls, then updates the position and velocity of all balls'''
	for index in range(len(ballList)):
		ball = ballList[index]
		if not ball.pstate: #only operate on non-pocketed balls
			ball.wallCollision(walls)
			ball.checkPocketed(pockets, 30)
			if index < len(ballList) - 1: # ensures no out of index error by checking collisions for the last ball in the list
				for ball2 in ballList[index + 1:]:
					if(ball.checkCollision(ball2)): # if collision happens, run collision and update ball status.
						vel1, vel2, ball.pos, ball2.pos = ball_collision(ball, ball2)
						ball.velMagnitude = math.sqrt(vel1[0]**2 + vel1[1]**2)
						ball.vel = [vel1[0]/ball.velMagnitude, vel1[1]/ball.velMagnitude] if ball.velMagnitude > 0 else [0, 0]
						ball2.velMagnitude = math.sqrt(vel2[0]**2 + vel2[1]**2)
						ball2.vel = [vel2[0]/ball2.velMagnitude, vel2[1]/ball2.velMagnitude]if ball2.velMagnitude > 0 else [0, 0]
	for ball in ballList:
		update(ball)
	return ballList















