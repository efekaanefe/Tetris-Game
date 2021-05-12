import pygame, random
from constants import *
from shape import *
import pygame.mixer

pygame.mixer.init()


class Game:

	def __init__(self, win, best_score):
		self.gameover = False
		self.score = 0
		self.best_score = best_score

		#main window
		self.win = win
		self.fps = FPS
		self.level = 0
		#for level update, not real count of pieces
		self.pieces = 0

		self.key_down_increase = False

		self.score_surface = self._create_score_surface()
		self.best_score_surface = self._create_best_score_surface()

		#playground
		self.playground_surface = self._create_playground_surface()
		self.playground_x = (SCREEN_WIDTH - PLAYGROUND_WIDTH) // 2 
		self.playground_y = SCREEN_HEIGHT - PLAYGROUND_HEIGHT
		self.inactive_shapes = []

		self.grids = []
		self.create_grids()
		
		#current moving shape
		self.next_shape = self.create_random_shape()
		self.current_shape = None
		self.update_current_and_next_shape()

		#keeps track of how mant rects there are in a row, in a inefficient way
		self.rects_in_rows = self.create_rects_in_rows()

		self.next_shape_surface = self._create_next_shape_surface()

	def update(self):
		self.blit_playground_surface()
		self.blit_score_surface()
		self.blit_best_score_surface()
		self._draw_text_on_win()
		self.blit_next_shape_surface()
		self.check_gameover()
		
		self.remove_rects_in_full_row()

		self.current_shape.update_activation_condition()
		self.update_inactive_shapes()
		self.update_level_and_fps()

		
		self.current_shape.move_shape_downward()
		self.current_shape.update_init()
		
		self.draw_active_shape()
		self.draw_inactive_shapes()
		self.draw_grids()

	def check_gameover(self):
		if self.rects_in_rows[0] != 0:
			print("Gameover!")
			self.gameover = True

	def key_down_fps_increase(self):
		self.fps += KEY_DOWN_FPS_CHANGE
		self.key_down_increase = True
	
	def key_down_fps_decrease(self):
		self.fps -= KEY_DOWN_FPS_CHANGE
		self.key_down_increase = False

	def update_level_and_fps(self):
		if self.pieces == PIECE_REQUIRED_TO_INCREASE_LEVEL:
			self.level += 1
			self.fps +=	FPS_INCREASE_ON_EACH_LEVEL
			self.pieces = 0

	def score_depending_on_level(self, removed_lines):
		lines = len(removed_lines)
		level = self.level
		line_multiplier = None
		if lines == 1:
			line_multiplier = 1
		elif lines == 2:
			line_multiplier = 2.5
		elif lines == 3:
			line_multiplier = 7.5
		else:
			line_multiplier = 30
		score = 40*(level+1)*line_multiplier
		print("level ", level,"lines ", line_multiplier)
		print("score ", score)
		return int(score)

	def _draw_text_on_win(self):
		text = TETRIS_FONT.render("TETRIS", 1, ORANGE)
		self.win.blit(text, ((SCREEN_WIDTH-text.get_width())//2,10))
		text = TETRIS_FONT.render("TETRIS", 1, PURPLE)
		self.win.blit(text, (2+(SCREEN_WIDTH-text.get_width())//2,2+10))

	def create_rects_in_rows(self):
		rects_in_rows = {}
		for row in range(PLAYGROUND_HEIGHT//SQUARE_SIZE):
			rects_in_rows[row] = 0
		return rects_in_rows

	def update_rects_in_rows(self):
		self.rects_in_rows = self.create_rects_in_rows()
		try:
			for shape in self.inactive_shapes:
				for rect in shape.rects:
					row = (rect.y-1)/SQUARE_SIZE
					self.rects_in_rows[row] += 1
		except KeyError:
			print("KeyError occured")

	def update_inactive_shapes(self):
		if self.current_shape.active == False:
			if self.key_down_increase:
				self.key_down_fps_decrease()
			self.rects_in_rows = self.create_rects_in_rows()
			#print(self.rects_in_rows)
			self.inactive_shapes.append(self.current_shape)
			self.update_current_and_next_shape()
			self.update_rects_in_rows()
			#print(self.rects_in_rows)
	
	def remove_flag(self):
		rows = self.rects_in_rows.keys()
		full_rows = []
		for r in rows:
			if self.rects_in_rows[r] == PLAYGROUND_WIDTH//SQUARE_SIZE:
				full_rows.append(r)
		return full_rows

	def shift_rects_after_remove(self, full_rows):
		remove_flag = full_rows
		if len(remove_flag) > 0:
			for shape in self.inactive_shapes:
				for rect in shape.rects:
					rect_row = (rect.y-1)/SQUARE_SIZE
					for row in remove_flag:
						if rect_row < row:
							# multiplier = self.shift_rect_until_collide(rect)
							# print(multiplier)
							# rect.y += multiplier*SQUARE_SIZE
							rect.y += SQUARE_SIZE
						else:
							continue

	def remove_rects_in_full_row(self):
		full_rows = self.remove_flag()
		if len(full_rows) > 0:
			pygame.mixer.Sound.play(CLEAR_LINE_SOUND_EFFECT)
			pygame.time.delay(50)
			for shape in self.inactive_shapes[::-1]:
				for rect in shape.rects[::-1]:
					rect_row = (rect.y-1)/SQUARE_SIZE
					if rect_row in full_rows:
						shape.remove_rect(rect)
			self.score += self.score_depending_on_level(full_rows)
			#self.remove_animation(full_rows)

			pygame.time.delay(200)
			self.shift_rects_after_remove(full_rows)
			self.update_rects_in_rows()

	# def remove_animation(self, full_rows):
	# 	rects = []
	# 	x = (SCREEN_WIDTH-PLAYGROUND_WIDTH)//2 
	# 	for row in full_rows:
	# 		y = (SCREEN_HEIGHT-PLAYGROUND_HEIGHT)+row*SQUARE_SIZE+1
	# 		rect = pygame.Rect(x, y, PLAYGROUND_WIDTH, SQUARE_SIZE)
	# 		rects.append(rect)
	# 	for rect in rects:
	# 		pygame.draw.rect(self.win, WHITE, rect)
	# 		pygame.display.update()
	# 		pygame.time.delay(50)
	# 	rects = []

	def create_random_shape(self):
		random_shape = random.choice(shapes)
		random_color = random.choice(shape_colors)

		return Shape(random_shape, random_color, -3, 4, self.inactive_shapes, self.grids)

	def update_current_and_next_shape(self):
		self.current_shape = self.next_shape
		self.next_shape = self.create_random_shape()
		self.pieces+=1

	def add_line_to_next_shape(self, rect, next_shape_surface):
		coordinates = [
						((rect.x, rect.y), (rect.x, rect.y+rect.height)),
						((rect.x, rect.y), (rect.x + rect.width, rect.y)),
						((rect.x+rect.width, rect.y), (rect.x+rect.width, rect.y+rect.height)),
						((rect.x+rect.width, rect.y+rect.height), (rect.x, rect.y+rect.height))]
		
		for coordinate in coordinates:
			pygame.draw.line(next_shape_surface, GREY, coordinate[0], coordinate[1])

	def _create_next_shape_surface(self):
		next_shape_surface = pygame.Surface((NEXT_SHAPE_WIDTH, NEXT_SHAPE_HEIGHT))	
		next_shape_surface.fill(BLACK)

		txt = TETRIS_FONT_2.render("NEXT", 1, ORANGE)
		next_shape_surface.blit(txt, ((NEXT_SHAPE_WIDTH-txt.get_width())//2,30))
		txt = TETRIS_FONT_2.render("NEXT", 1, PURPLE)
		next_shape_surface.blit(txt, (2+(NEXT_SHAPE_WIDTH-txt.get_width())//2,2+30))

		shape = self.next_shape

		#for center rect
		x_center = NEXT_SHAPE_WIDTH//2 - SQUARE_SIZE//4
		y_center = NEXT_SHAPE_HEIGHT//2 + 10

		rect = pygame.Rect(x_center, y_center, SQUARE_SIZE//2, SQUARE_SIZE//2)
		pygame.draw.rect(next_shape_surface, shape.color, rect)
		self.add_line_to_next_shape(rect, next_shape_surface)

		#other rects
		for (row_change, col_change) in shape.shape[0]:
			y_change = row_change * SQUARE_SIZE//2
			x_change = col_change * SQUARE_SIZE//2

			x = x_center - x_change
			y = y_center - y_change

			rect = pygame.Rect(x, y, SQUARE_SIZE//2, SQUARE_SIZE//2)

			pygame.draw.rect(next_shape_surface, shape.color, rect)
			self.add_line_to_next_shape(rect, next_shape_surface)


		pygame.display.update()

		return next_shape_surface

	def blit_next_shape_surface(self):
		self.next_shape_surface = self._create_next_shape_surface()
		self.win.blit(self.next_shape_surface, (50+self.playground_x+PLAYGROUND_WIDTH, 75+self.playground_y+250))

	def _create_best_score_surface(self):
		best_score_surface = pygame.Surface((BEST_SCORE_WIDTH,BEST_SCORE_HEIGHT))
		best_score_surface.fill(BLACK)

		txt = BEST_SCORE_FONT.render("BEST SCORE", 1, ORANGE)
		best_score_surface.blit(txt, ((BEST_SCORE_WIDTH-txt.get_width())//2,40))
		txt = BEST_SCORE_FONT.render("BEST SCORE", 1, PURPLE)
		best_score_surface.blit(txt,(2+(BEST_SCORE_WIDTH-txt.get_width())//2,2+40))

		score = BEST_SCORE_FONT.render(str(self.best_score), 1, ORANGE)
		best_score_surface.blit(score, ((BEST_SCORE_WIDTH-score.get_width())//2,75))
		score = BEST_SCORE_FONT.render(str(self.best_score), 1, PURPLE)
		best_score_surface.blit(score, (2+(BEST_SCORE_WIDTH-score.get_width())//2,2+75))
		
		return best_score_surface

	def blit_best_score_surface(self):
		self.win.blit(self.best_score_surface, (BEST_SCORE_X, BEST_SCORE_Y))

	def _create_score_surface(self): #includes level
		score_surface = pygame.Surface((SCORE_WIDTH, SCORE_HEIGHT+100))
		score_surface.fill(pygame.Color("black"))

		txt = SCORE_FONT.render("SCORE", 1, ORANGE)
		score_surface.blit(txt, ((SCORE_WIDTH-txt.get_width())//2,40))
		txt = SCORE_FONT.render("SCORE", 1, PURPLE)
		score_surface.blit(txt,(2+(SCORE_WIDTH-txt.get_width())//2,2+40))

		score = SCORE_FONT.render(str(self.score), 1, ORANGE)
		score_surface.blit(score, ((SCORE_WIDTH-score.get_width())//2,75))
		score = SCORE_FONT.render(str(self.score), 1, PURPLE)
		score_surface.blit(score, (2+(SCORE_WIDTH-score.get_width())//2,2+75))
		
		shift = 75
		txt = LEVEL_FONT.render("LEVEL", 1, ORANGE)
		score_surface.blit(txt, ((SCORE_WIDTH-txt.get_width())//2,shift+40))
		txt = LEVEL_FONT.render("LEVEL", 1, PURPLE)
		score_surface.blit(txt,(2+(SCORE_WIDTH-txt.get_width())//2,shift+2+40))

		score = LEVEtxt = LEVEL_FONT.render(str(self.level), 1, ORANGE)
		score_surface.blit(score, ((SCORE_WIDTH-score.get_width())//2,shift+75))
		score = LEVEtxt = LEVEL_FONT.render(str(self.level), 1, PURPLE)
		score_surface.blit(score, (2+(SCORE_WIDTH-score.get_width())//2,shift+2+75))

		return score_surface

	def blit_score_surface(self):
		if self.score % 10 == 0:
			self.score_surface = self._create_score_surface()	
			self.win.blit(self.score_surface, (self.playground_x+PLAYGROUND_WIDTH+50, self.playground_y+100))

			pygame.display.update()

	def _create_playground_surface(self):
		playground_surface = pygame.Surface((PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT))
		playground_surface.fill(pygame.Color("black"))

		#lines
		for x in range(SQUARE_SIZE, SCREEN_HEIGHT, SQUARE_SIZE):

			pygame.draw.line(playground_surface, pygame.Color("grey"), (x, 0), (x, PLAYGROUND_HEIGHT))

		for y in range(SQUARE_SIZE, SCREEN_WIDTH, SQUARE_SIZE):
			pygame.draw.line(playground_surface, pygame.Color("grey"), (0, y), (PLAYGROUND_WIDTH, y))

		return playground_surface

	def blit_playground_surface(self):
		self.win.blit(self.playground_surface, (self.playground_x, self.playground_y))
		pygame.display.update()

	def create_grids(self):
		grid1 = pygame.Rect(self.playground_x-GRID_SIZE, self.playground_y-GRID_SIZE, GRID_SIZE, VERTICAL_GRID_LENGTH)
		grid2 = pygame.Rect(self.playground_x, self.playground_y-GRID_SIZE, HORIZONTAL_GRID_LENGTH, GRID_SIZE)
		grid3 = pygame.Rect(self.playground_x+PLAYGROUND_WIDTH, self.playground_y, GRID_SIZE, VERTICAL_GRID_LENGTH-GRID_SIZE)

		#for score surface
		x = self.playground_x+PLAYGROUND_WIDTH+50-2
		y = self.playground_y+100-2
		width = SCORE_WIDTH+2
		height = SCORE_HEIGHT + NEXT_SHAPE_HEIGHT + 75+2
		thickness = 2
		grid4 = pygame.Rect(x, y, width, thickness)
		grid5 = pygame.Rect(x, y, thickness, height)
		grid6 = pygame.Rect(x, y+height, width, thickness)
		grid7 =pygame.Rect(x+width, y, thickness, height+2)

		#for best score surface
		x = BEST_SCORE_X-2
		y = BEST_SCORE_Y-2
		width = BEST_SCORE_WIDTH+2
		height = BEST_SCORE_HEIGHT + 2
		thickness = 2
		grid8 = pygame.Rect(x, y, width, thickness)
		grid9 = pygame.Rect(x, y, thickness, height)
		grid10 = pygame.Rect(x, y+height, width, thickness)
		grid11 =pygame.Rect(x+width, y, thickness, height+2)
		
		

		self.grids =[grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9, grid10, grid11]

	def draw_grids(self):
		for grid in self.grids:
			pygame.draw.rect(self.win, (255,0,0), grid)

	def draw_active_shape(self):
		self.playground_surface = self._create_playground_surface()
		for rect in self.current_shape.rects:
			pygame.draw.rect(self.playground_surface, self.current_shape.color, rect)
			pygame.display.update()

	def draw_inactive_shapes(self):
		for shape in self.inactive_shapes:
			for rect in shape.rects:
				pygame.draw.rect(self.playground_surface, shape.color, rect)
				pygame.display.update()


