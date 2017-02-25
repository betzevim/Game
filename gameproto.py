import pygame, math, sys, random

from pygame.locals import *
screen = pygame.display.set_mode((1280, 748))

pygame.init()

clock = pygame.time.Clock()
FRAMES_PER_SECOND = 30

x = 0
y = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('arial', 18)


balls = []

ball_rad = 20

x_speed = 0
y_speed = 0
x_accel = 0
y_accel = 0
friction = 0.85

lev = 0

lives = 1 # increase this to make the game easier

def constrain(val, minny, maxxy):
	if minny > val: return minny
	if maxxy < val: return maxxy
	return val

def addball(Type):
	x = random.randrange(300, screen.get_width() - ball_rad)
	y = random.randrange(300, screen.get_height() - ball_rad)
	if Type == 1:
		x = screen.get_width() - 100
		y = screen.get_height() - 100
		color = (0, 0, 0)
	if Type == 2:
		color = (255, 0, 0)
	if Type == 3:
		color = (255, 255, 0)
	if Type == 4:
		color = (245, 245, 245)
	ball = {
		'Type':Type,
		'color':color,
		'xsp':5,
		'ysp':5,
		'x':x,
		'y':y
	}
	balls.append(ball)



sld = 0

def reset_balls(lev_up):
	del balls[:]
	global lev, x, y, font, B_slow, B_live, sld, dmgB
	screen.fill((BLACK))
	sld = 1
	pygame.display.flip()
	clock.tick(FRAMES_PER_SECOND)
	screen.fill(WHITE)
	pygame.display.flip()
	clock.tick(FRAMES_PER_SECOND)
	if lev_up:
		lev += 1
		dmgB = lev
		B_slow = int(lev / 2) + 1
		B_live = int(lev / 4) + 1
	for i in range(B_slow):
		addball(3)
	for i in range(B_live):
		addball(4)
	addball(1)
	x = 0
	y = 0
	for i in range(dmgB):
		addball(2)


def change_sp(num):
	for ball in balls:
		ball['xsp'] = num
		ball['ysp'] = num


reset_balls(True)

while 1:
	deltat = clock.tick(FRAMES_PER_SECOND)
	pygame.event.pump()
	x_accel = x_speed * 0.1
	y_accel = y_speed * 0.1
	x_accel = abs(x_accel)
	y_accel = abs(y_accel)
	x_accel = constrain(x_accel, 3, 5)
	y_accel = constrain(y_accel, 3, 5)
	Xkeys = pygame.key.get_pressed()
	if Xkeys[K_RIGHT]: x_speed += x_accel
	if Xkeys[K_LEFT]: x_speed -= x_accel
	if Xkeys[K_UP]: y_speed -= y_accel
	if Xkeys[K_DOWN]: y_speed += y_accel
	if Xkeys[K_ESCAPE]: sys.exit(0)
	x_speed *= friction
	y_speed *= friction
	x += x_speed
	y += y_speed
	x_speed = constrain(x_speed, -20, 20)
	y_speed = constrain(y_speed, -20, 20)
	screen.fill(WHITE)
	delete = 0
	cntdwn = ''
	if sld > 0:
		sld -= 1
		if sld == 0:
			change_sp(10) 
	del_slow = False
	for ball in balls:
		ball['x'] += ball['xsp']
		ball['y'] += ball['ysp']
		if ball['x'] < ball_rad or ball['x'] >= (screen.get_width() - ball_rad) or random.uniform(1, 50) < 1.5:
			ball['xsp'] *= -1
		if ball['y'] < ball_rad or ball['y'] >= (screen.get_height() - ball_rad) or random.uniform(1, 50) < 1.5:
			ball['ysp'] *= -1
		ball['x'] = constrain(ball['x'], ball_rad, screen.get_width() - ball_rad)
		ball['y'] = constrain(ball['y'], ball_rad, screen.get_height() - ball_rad)
		pygame.draw.circle(screen, ball['color'], (int(ball['x']),int(ball['y'])), ball_rad)
		xdis = x - ball['x']
		ydis = y - ball['y']
		if ydis * ydis + xdis * xdis < ball_rad * 4 * ball_rad:
			if ball['Type'] == 1:
				reset_balls(True)
			elif ball ['Type'] == 3:
				sld += 400
				change_sp(5)
				del_slow = True
			elif ball['Type'] == 4:
				B_live -= 1
				if lives < 10:
					lives += 1
				delete = ball
			else:
				lives -= 1
				dmgB -= 1
				reset_balls(False)
				if lives < 1:
					sys.exit(0)
	if delete != 0: balls.remove(delete)
	if del_slow:
		for i in reversed(range(len(balls))):
			if balls[i]['Type'] == 3:
				balls.remove(balls[i])
	if sld > 0:
		cntdwn = '  DECREASED SPEED FOR ' + str(sld / FRAMES_PER_SECOND)
	text = font.render('LEVEL: ' + str(lev) + '  LIVES: ' + str(lives) + cntdwn, False, (0, 0, 0))
	screen.blit(text, (0, 0))
	x = constrain(x, ball_rad, screen.get_width() - ball_rad)
	y = constrain(y, ball_rad, screen.get_height() - ball_rad)
	pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), ball_rad)
	pygame.display.flip()