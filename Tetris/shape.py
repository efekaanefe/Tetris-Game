
import pygame
from constants import *

class Shape:

    def __init__(self, shape, color, row, col, inactive_shapes, grids):
        self.color = color
        self.shape = shape
        self.row = row
        self.col = col


        self.inactive_shapes = inactive_shapes
        self.grids = grids


        self.x = self.col*SQUARE_SIZE +1
        self.y = self.row*SQUARE_SIZE +1
        self.SQUARE_SIZE = SQUARE_SIZE -1

        self.active = True

        self.rotation = 0
        
        self.center_rect = pygame.Rect(self.x, self.y, self.SQUARE_SIZE, self.SQUARE_SIZE)
        self.rects = []
        self.create_other_rects()

        #self.moveable_right = True
        #self.moveable_left = True
        #self.rotatable = True
    
    def update_init(self):
        #for center square
        self.x = self.rects[0].x
        self.y = self.rects[0].y
        # self.moveable_right = True
        # self.moveable_left = True
        # self.rotatable = True

    def update_activation_condition(self):
        for rect in self.rects:
            tmp_rect = pygame.Rect(rect.x, rect.y+SQUARE_SIZE, SQUARE_SIZE-1, SQUARE_SIZE-1)
            if len(self.inactive_shapes) != 0:
                for inactive_shape in self.inactive_shapes:
                    for inactive_rect in inactive_shape.rects:
                        if tmp_rect.colliderect(inactive_rect):
                            self.make_inactive()
                            return True
                        else:
                            pass        
        return False

    def make_inactive(self):
            self.active = False

    def rotatable(self):
        ghost_rects = [self.center_rect]
        for (row_change, col_change) in self.shape[(self.rotation+1) % len(self.shape)]:
            y_change = row_change * SQUARE_SIZE
            x_change = col_change * SQUARE_SIZE

            x = self.x - x_change
            y = self.y - y_change

            rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)

            ghost_rects.append(rect)

        for ghost_rect in ghost_rects:
            for inactive_shape in self.inactive_shapes:
                for inactive_rect in inactive_shape.rects:
                    if ghost_rect.colliderect(inactive_rect) or ghost_rect.y > PLAYGROUND_HEIGHT:
                        print("You can´t rotate")
                        return False
                    #if rotate makes a shape go out off playgroundscreen, it shouldn´t rotate
                    #but if it is possible to rotate the piece after shifting the center square
                    #it should rotate
                    elif not 0 <= ghost_rect.x < PLAYGROUND_WIDTH: 
                        print("You can´t rotate")
                        return False

        return True

    def rotate(self):
        if self.rotatable():
            self.update_init()
            self.rotation += 1
            try:
                self.rotation = self.rotation % len(self.shape)
                self.create_other_rects()
            except ZeroDivisionError:
                print("ZeroDivisionError")

    #player wont unrotate
    def unrotate(self):
        self.update_init()
        self.rotation -= 1
        try:
            self.rotation = self.rotation % len(self.shape)
            self.create_other_rects()
        except ZeroDivisionError:
            print("ZeroDivisionError")

    def create_other_rects(self):
        rects = [self.center_rect] 
        for (row_change, col_change) in self.shape[self.rotation]:
            y_change = row_change * SQUARE_SIZE
            x_change = col_change * SQUARE_SIZE

            x = self.x - x_change
            y = self.y - y_change

            rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)

            rects.append(rect)

        self.rects = rects

    def remove_rect(self, rect):
        self.rects.remove(rect)

    """ Movement flag functions """
    def moveable_down(self):
        for rect in self.rects:
            if rect.y + SQUARE_SIZE >= PLAYGROUND_HEIGHT:
                return False
        return True
    
    def moveable_left(self):
        for rect in self.rects:
            if rect.x - SQUARE_SIZE < 0:
                return False
            else:
                for shape in self.inactive_shapes:
                    for inactive_rect in shape.rects:
                        if rect.y == inactive_rect.y:
                            if rect.x - SQUARE_SIZE == inactive_rect.x:
                                return False
        return True
    
    def moveable_right(self):
        for rect in self.rects:
            if rect.x + SQUARE_SIZE > PLAYGROUND_WIDTH:
                return False
            else:
                for shape in self.inactive_shapes:
                    for inactive_rect in shape.rects:
                        if rect.y == inactive_rect.y:
                            if rect.x + SQUARE_SIZE == inactive_rect.x:
                                return False
        return True

    """ Move Functions """
    def move_shape_downward(self):
        if self.moveable_down():
            for rect in self.rects:
                rect.y += SQUARE_SIZE
        else:
            self.make_inactive()

    def move_shape_upward(self):
        if self.active:
            for rect in self.rects:
                rect.y -= SQUARE_SIZE
        
    def move_shape_leftward(self):
        if self.moveable_left():
            for rect in self.rects:
                rect.x -= SQUARE_SIZE
                
    def move_shape_rightward(self):
        if self.moveable_right():
            for rect in self.rects:
                rect.x += SQUARE_SIZE
    