import pygame, sys
from game import Game
from shape import shapes, shape_colors, Shape
from constants import *
import pygame.mixer

pygame.mixer.init()

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.font.init()

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
WIN.fill(pygame.Color("black"))
#WIN.blit(BACKGROUND_IMAGE, (0,0))



def main(best_score):
	global WIN
	GAME = Game(WIN, best_score)
	clock = pygame.time.Clock() 
	
	gameover = False
	while not gameover:
		clock.tick(GAME.fps)
		
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				gameover = True
				sys.exit()


			elif event.type == pygame.KEYDOWN:

				if event.key == pygame.K_RIGHT and GAME.current_shape.active:
					GAME.current_shape.move_shape_rightward()

				elif event.key == pygame.K_LEFT and GAME.current_shape.active:
					GAME.current_shape.move_shape_leftward()
					
				elif event.key == pygame.K_UP:
					GAME.current_shape.rotate()
				
				elif event.key == pygame.K_DOWN:
					if GAME.current_shape.time_increment == TIME_INCREMENT:
						GAME.current_shape.time_increment *= 5 + GAME.level
				#inactivates current shape
				elif event.key == pygame.K_SPACE:
					GAME.current_shape.make_inactive()
					
		GAME.update()		
		pygame.display.update()
		#print(GAME.gameover)

		if GAME.gameover:
			#drawing gameover text and score
			gameover_text(GAME, best_score)
			gameover = True

			write_best_score(GAME.score)

			#setting up the window again for new game
			WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.display.set_caption("Tetris")
			WIN.fill(pygame.Color("black"))
			main_menu()



def main_menu(): 
	best_score = read_best_score()
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
				WIN.blit(BACKGROUND_IMAGE, (0,0))
				best_score = read_best_score()
				main(best_score)
				run = False

		draw_main_menu_text()
		pygame.display.update()


#returns best score
def read_best_score():
	file = open("bestscore.txt", "r")
	best_score = int(file.readline())
	file.close()
	return best_score

#overwrites best score
def write_best_score(score):
	file = open("bestscore.txt", "w")
	file.write(str(score))

def gameover_text(GAME, best_score):
	WIN.fill(GREY)
	if GAME.score < best_score:
		text = "Gameover! Your score:"
	else:
		text = "Congratulations! New best score:"
	draw_text = GAMEOVER_FONT.render(text, 1, ORANGE)
	WIN.blit(draw_text, (SCREEN_WIDTH/2 - draw_text.get_width() /
						 2, SCREEN_HEIGHT/2 - draw_text.get_height()/2))
	score = str(GAME.score)
	score_text = GAMEOVER_FONT.render(score, 1, ORANGE)
	WIN.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width() /
						 2, 100+SCREEN_HEIGHT/2 - score_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(5000)

def draw_main_menu_text():
	text = TETRIS_FONT.render("WELCOME TO", 1, ORANGE)
	WIN.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height()-150)//2))
	text = TETRIS_FONT.render("WELCOME TO", 1, RED)
	WIN.blit(text, (2+(SCREEN_WIDTH-text.get_width())//2,2+(SCREEN_HEIGHT-text.get_height()-150)//2))
	text = TETRIS_FONT.render("TETRIS", 1, ORANGE)
	WIN.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height())//2))
	text = TETRIS_FONT.render("TETRIS", 1, RED)
	WIN.blit(text, (2+(SCREEN_WIDTH-text.get_width())//2,2+(SCREEN_HEIGHT-text.get_height())//2))
	
	txt = "by Ahmet Efekaan Efe"
	text = TETRIS_FONT_3.render(txt, 1, GREY)
	WIN.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(100+SCREEN_HEIGHT-text.get_height())//2))
	text = TETRIS_FONT_3.render(txt, 1, WHITE)
	WIN.blit(text, (2+(SCREEN_WIDTH-text.get_width())//2,2+(100+SCREEN_HEIGHT-text.get_height())//2))

	text = TETRIS_FONT_2.render("press any key to play", 1, GREY)
	WIN.blit(text, ((SCREEN_WIDTH-text.get_width()-2)//2,(SCREEN_HEIGHT-text.get_height()-2)-300//2))
	text = TETRIS_FONT_2.render("press any key to play", 1, WHITE)
	WIN.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height())-300//2))

main_menu()
#main(0)