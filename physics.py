#will take in list of ball objects and current cue position/direction, output end state of balls
#later will output lines for projected ball motions

# READ
# READ
# READ
# READ
# READ
# We do not actually have to implement physics in terms of "actual" physics (eg. forces, friction, etc.), but simply a simulation that will model similar effects.
# Basically, we only need balls to have a "velocity" in x and y components that will decay over time
import numpy as np
import ball, math

'''currently uneccessary'''
# class line(object):
# 	# draw lines
# 	def __init__(self, width = 1, color = pygame.Color('white'), table, start, end):
# 		self.width = width
# 		self.color = color
# 		self.table = table
# 		self.start = start
# 		self.end = end
# 	def draw(self):
# 		pygame.draw.line(self.table, 
# 						 self.color,
# 						 self.start,
# 						 self.end,
# 						 self.width)

def update(ball1):
	# Update ball position
	step = .2
	ball1.pos = [ball1.pos[0] + ball1.vel[0] * step, ball1.pos[1] + ball1.vel[1] * step] # updating ball positions based on velocity
	if abs(ball1.vel[0]) > 0:
		if abs(ball1.vel[0]) < step:
			ball1.vel[0] = 0
		else:
			ball1.vel[0] += step if ball1.vel[0] < 0 else (-1 * step) # decreasing velocity
	if abs(ball1.vel[1]) > 0:
		if abs(ball1.vel[1]) < step:
			ball1.vel[1] = 0
		else:
			ball1.vel[1] += step if ball1.vel[1] < 0 else -1 * step
	return ball1

def ball_collision(ball_1, ball_2): 
		# Calculate velocity after collision between two balls
	m1 = ball_1.mass
	m2 = ball_2.mass
	pos_1 = np.array(ball_1.pos)
	pos_2 = np.array(ball_2.pos)
	vel_1 = np.array(ball_1.vel)
	vel_2 = np.array(ball_2.vel)

	n = pos_2 - pos_1
	un = n / math.sqrt(np.dot(n,n))
	ut = np.array(-un[1],un[0])

	vel_1n = np.dot(un, vel_1) # use numpy's dot, not vdot
	vel_1t = np.dot(ut, vel_1)
	vel_2n = np.dot(un, vel_2)
	vel_2t = np.dot(ut, vel_2)

	new_vel_1t = vel_1t * ut
	new_vel_2t = vel_2t * ut
	new_vel_1n = (vel_1n*(m1-m2) + 2*m2*vel_2n)/(m1+m2) * un
	new_vel_2n = (vel_2n*(m2-m1) + 2*m1*vel_1n)/(m1+m2) * un

	new_vel_1 = new_vel_1n + new_vel_1t
	new_vel_2 = new_vel_2n + new_vel_2t

	return [list(new_vel_1), list(new_vel_2)]
		
def run(ballList, walls, pockets):
	for index in range(len(ballList)):
		ball = ballList[index]
		if not ball.pstate: #only operate on non-pocketed balls
			ball.wallCollision(walls)
			ball.checkPocketed(pockets, 4)
			if index < len(ballList) - 1: # ensures no out of index error by checking collisions for the last ball in the list
				for ball2 in ballList[index + 1:]:
					if(ball.checkCollision(ball2)):
						ball.vel, ball2.vel = ball_collision(ball, ball2)
	for ball in ballList:
		update(ball)
	return ballList















