import pygame
from abc import ABC, abstractmethod
import math
import time
import random

width, height = 1200, 900

screen = pygame.display.set_mode((width, height))

ende = False

fps = 60

fallspeed = 10

falltime = 0.02

blocksize = 20

movetime = 0.01

penice_chance = 50

movespeed = blocksize

clock = pygame.time.Clock()

time_between_rotate = 0.1#in seconds

pygame.display.set_caption("Bugged Tetris")

img = pygame.image.load("tetris.png")
pygame.display.set_icon(img)



"""
everything for gamefloor
"""
gamefloor_x, gamefloor_y, gamefloor_width, gamefloor_height = width//4, height//16, (width//2//blocksize)*blocksize, blocksize*40

gamefloor_color = (128, 128, 128)

all_choice_x = [el for el in range(gamefloor_x, gamefloor_x+gamefloor_width, blocksize)]


class PhysicObject(ABC):
    pass

class Hitbox:

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def is_colliding(self, other):
        """

        checks if colliding with other hitbox
        """
        statements = []
        statements.append((self.x >= other.x and self.x+self.width <= other.x+other.width and self.y >= other.y and self.y <= other.y+other.height))
        statements.append((self.x+self.width >= other.x and self.x+self.width <= other.x+other.width and self.y >= other.y and self.y <= other.y+other.height))
        statements.append((self.x >= other.x and self.x <= other.x+other.width and self.y+self.height >= other.y and self.y+self.height <= other.y+other.height))
        statements.append((self.x+self.width >= other.x and self.x+self.width <= other.x+other.width and self.y+self.height >= other.y and self.y+self.height <= other.y+other.height))

        return any(statements)


class Block(PhysicObject):
    def __init__(self, x, y, blocksize, color):
        self.__x, self.__y = x, y
        self.blocksize = blocksize
        self.width, self.height = self.blocksize, self.blocksize
        self.color = color
        self.hitbox = Hitbox(self.__x, self.__y, self.blocksize, self.blocksize)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.blocksize, self.blocksize))

    def set_x(self, val):
        self.x = val
        self.hitbox.x = val

    def set_y(self, val):
        self.y = val
        self.hitbox.y = val

    def move_right(self, val):
        self.set_x(self.x+val)

    def move_up(self, val):
        self.set_y(self.y+val)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, val):
        self.__x = val
        self.hitbox.x = val

    @y.setter
    def y(self, val):
        self.__y = val
        self.hitbox.y = val

class Tetris_Construct(ABC):

    """
    class that defines tetris structure
    """

    def __init__(self, x, y, color, blocks=[]):
        self.x, self.y = x, y
        #all blocks that are inside tetris construct
        self.blocks = blocks
        self.color = color

        #pointer to angle block
        self.angle_block = None

        self.right_blocks = []
        self.down_blocks = []
        self.left_blocks = []
        self.up_blocks = []

        """
        0: topleft
        1: topright
        2: downright
        3: downleft

        -> 0
        """
        self.old_angle_position = 0
        self.angle_position = 0



    def rotate_left(self, gf):
        """
        rotates all inner blocks around origin block to right
        """

        lowest = self.find_lowest()
        if (lowest.x-(lowest.y-self.angle_block.y + (lowest.x-self.angle_block.x))) <= gf.x:
            return

        highest = self.find_highest()
        if (highest.x + ((self.angle_block.y-highest.y) - (self.angle_block.x-highest.x))) >= gf.x+gf.width:
            return

        leftest = self.find_leftest()

        if (leftest.y - (self.angle_block.x-leftest.x) + (leftest.y-self.angle_block.y)) < gf.y-2*blocksize:
            return

        rightest = self.find_rightest()

        if (rightest.y + (rightest.x-self.angle_block.x) + (self.angle_block.y-rightest.y)) >= gf.y+gf.height-blocksize:
            return

        for el in self.down_blocks:
            xexpression = (el.y-self.angle_block.y + (el.x-self.angle_block.x))
            yexpression = (el.y-self.angle_block.y -(el.x-self.angle_block.x))
            el.y += -yexpression
            el.x += -xexpression

        for el in self.left_blocks:
            yexpression = (self.angle_block.x-el.x + (el.y-self.angle_block.y))
            xexpression = (self.angle_block.x-el.x - (el.y-self.angle_block.y))
            el.x += xexpression
            el.y += -yexpression

        for el in self.up_blocks:
            yexpression = (self.angle_block.y-el.y - (self.angle_block.x-el.x))
            xexpression = (self.angle_block.y-el.y + (self.angle_block.x-el.x))
            el.x += xexpression
            el.y += yexpression

        for el in self.right_blocks:
            yexpression = (el.x-self.angle_block.x+self.angle_block.y-el.y)
            xexpression = (el.x-self.angle_block.x-(self.angle_block.y-el.y))
            el.x  += -xexpression
            el.y += yexpression


        speicher = self.up_blocks
        self.up_blocks = self.left_blocks
        self.left_blocks = self.down_blocks
        self.down_blocks = self.right_blocks
        self.right_blocks = speicher


        #getting x for the mostleft block
        self.find_new_coords()

    def rotate_right(self, gf):
        """
        rotates all inner blocks around origin block to right
        """

        lowest = self.find_lowest()
        if (lowest.x - ((lowest.x-self.angle_block.x) - (lowest.y-self.angle_block.y))) >= gf.x+gf.width:
            return

        highest = self.find_highest()
        if (highest.x - ((self.angle_block.y-highest.y - (self.angle_block.x-highest.x)))) <= gf.x:
            return

        rightest = self.find_rightest()
        if (rightest.y - (((rightest.x-self.angle_block.x)+(rightest.y-self.angle_block.y)))) <= gf.y:
            return

        leftest = self.find_leftest()
        if (leftest.y - (( (leftest.x-self.angle_block.x) + (leftest.y-self.angle_block.y)))) >= gf.y+gf.height:
            return

        for el in self.down_blocks:
            xexpression = ((el.x-self.angle_block.x) - (el.y-self.angle_block.y) )
            yexpression = ( (el.x-self.angle_block.x) + (el.y-self.angle_block.y))
            el.y += -yexpression
            el.x += -xexpression

        for el in self.left_blocks:
            xexpression = (self.angle_block.x-el.x + (el.y-self.angle_block.y))
            yexpression = ((self.angle_block.x-el.x) - (el.y-self.angle_block.y))
            el.x += xexpression
            el.y += yexpression

        for el in self.up_blocks:
            xexpression = (self.angle_block.y-el.y - (self.angle_block.x-el.x))
            yexpression = ((self.angle_block.y-el.y)+(self.angle_block.x-el.x))
            el.x += -xexpression
            el.y += yexpression

        for el in self.right_blocks:
            xexpression = (el.x-self.angle_block.x - (el.y - self.angle_block.y))
            yexpression = ((el.x-self.angle_block.x)+(el.y-self.angle_block.y))
            el.x  -= xexpression
            el.y += -yexpression


        speicher = self.right_blocks
        self.right_blocks = self.down_blocks
        self.down_blocks = self.left_blocks
        self.left_blocks = self.up_blocks
        self.up_blocks = speicher


        #getting x for the mostleft block
        self.find_new_coords()


    def find_new_coords(self):
        """
        finds new x and y
        """
        if self.left_blocks:
            x_val = 10000
            element = None
            for el in self.left_blocks:
                if el.x <= x_val:
                    element = el
                    x_val = el.x
            self.x, self.y = el.x, el.y
            return
        elif self.up_blocks:
            y_val = 10000
            element = None
            for el in self.up_blocks:
                if el.y <= y_val:
                    element = el
                    y_val = el.y
            self.x, self.y = el.x, el.y
            return
        else:
            self.x, self.y = self.angle_block.x, self.angle_block.y




    def set_angle_block(self, block):
        """
        sets the corner of the block that should be rotating around itself
        """
        self.angle_block = block

    @abstractmethod
    def add_blocks(self):
        pass

    def draw(self, screen):
        for el in self.blocks:
            el.draw(screen)

    def find_rightest(self):

        """
        finds rightest value of all blocks
        """
        val = 0
        element = None
        for el in self.blocks:
            if el.x >= val:
                element = el
                val = el.x
        return element

    def find_leftest(self):

        """
        finds mostleft block
        """
        val = 10000
        element = None
        for el in self.blocks:
            if el.x <= val:
                element = el
                val = el.x
        return element

    def find_highest(self):
        """
        finds hgihest block in structure
        """
        val = 10000
        element = None
        for el in self.blocks:
            if el.y <= val:
                val = el.y
                element = el
        return element

    def find_lowest(self):
        """
        finds lowest block
        """
        val = 0
        element = None
        for el in self.blocks:
            if el.y > val:
                val = el.y
                element = el
        return element


    def move_up(self, speed, gf):
        """

        moves up the speed in block direction gf = gamefloor

        """

        highest = self.find_highest()
        lowest = self.find_lowest()

        if (speed <= 0 and not highest.y <= gf.y) or (speed >= 0 and not lowest.y+blocksize >= gf.y+gf.height):
            for el in self.blocks:
                el.y += speed

    def move_right(self, speed, gf):
        """

        moves all blocks right

        gf = gamefloor

        """
        rightest = self.find_rightest()
        leftest = self.find_leftest()
        if (speed <= 0 and not leftest.x <= gf.x) or (speed >= 0 and not rightest.x+blocksize >= gf.x+gf.width):
            for el in self.blocks:
                el.x += speed

    """
    setter methods
    """
    def setx(self, val):
        self.x = val
        for el in self.blocks:
            el.x = val+(el.x-self.x)
        self.x = val

    def sety(self, val):
        for el in self.blocks:
            el.y = val+(el.y-self.y)
        self.y = val


"""
for rotation regulation
"""
class RotationRegulator:

    def __init__(self, time_in_between):
        """
        regulates rotation
        """
        self.time_in_between = time_in_between
        self.last_time = time.perf_counter()
        self.curr_time = time.perf_counter()

    def can_rotate(self):
        """
        checks if rotation is valid
        """
        self.curr_time = time.perf_counter()
        if self.curr_time-self.last_time >= self.time_in_between:
            self.last_time = self.curr_time
            return True
        else:
            return False





class Long(Tetris_Construct):

    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 255))
        self.add_blocks()

    def add_blocks(self):
        """
        adds all the long blocks
        """
        b1 = Block(self.x, self.y, blocksize, self.color)
        b2 = Block(self.x, self.y+blocksize, blocksize, self.color)
        b3 = Block(self.x, self.y+2*blocksize, blocksize, self.color)
        b4 = Block(self.x, self.y+3*blocksize, blocksize, self.color)

        #setting all needed blocks
        self.blocks = [b1, b2, b3, b4]
        self.angle_block = b1
        self.down_blocks = [b2, b3, b4]

class Cube(Tetris_Construct):

    def __init__(self, x, y):
        super().__init__(x, y, (20, 140, 250))
        self.add_blocks()

    def add_blocks(self):

        """
        adds all blocks in square form
        """
        b1 = Block(self.x, self.y, blocksize, self.color)
        b2 = Block(self.x+blocksize, self.y, blocksize, self.color)
        b3 = Block(self.x, self.y+blocksize, blocksize, self.color)
        b4 = Block(self.x+blocksize, self.y+blocksize, blocksize, self.color)

        #setting all needed blocks
        self.blocks = [b1, b2, b3, b4]
        self.angle_block = b1

    def rotate_left(self, a):
        pass

    def rotate_left(self, a):
        pass

class Corner(Tetris_Construct):

    def __init__(self, x, y):
        super().__init__(x, y, (229, 148, 0))
        self.add_blocks()

    def add_blocks(self):

        """
        adds all blocks in corner form
        """
        b1 = Block(self.x, self.y, blocksize, self.color)
        b2 = Block(self.x+blocksize, self.y, blocksize, self.color)
        b3 = Block(self.x+blocksize, self.y-blocksize, blocksize, self.color)
        b4 = Block(self.x+blocksize, self.y-2*blocksize, blocksize, self.color)
        b5 = Block(self.x-blocksize, self.y, blocksize, self.color)

        #setting all needed blocks
        self.blocks = [b1, b2, b3, b4, b5]
        self.angle_block = b1
        self.right_blocks = [b2, b3, b4]
        self.left_blocks = [b5]

class Stairs(Tetris_Construct):

    def __init__(self,x, y):
        super().__init__(x, y, (65, 255, 110))
        self.add_blocks()

    def add_blocks(self):
        """
        adds blocks in stairs form
        """
        b1 = Block(self.x-blocksize, self.y+blocksize, blocksize, self.color)
        b2 = Block(self.x, self.y+blocksize, blocksize, self.color)
        b3 = Block(self.x, self.y, blocksize, self.color)
        b4 = Block(self.x+blocksize, self.y, blocksize, self.color)
        b5 = Block(self.x+blocksize, self.y-blocksize, blocksize, self.color)

        self.blocks = [b1, b2, b3, b4, b5]
        self.angle_block = b3
        self.down_blocks = [b1, b2]
        self.right_blocks = [b4, b5]

class Penice(Tetris_Construct):

    def __init__(self, x, y):
        super().__init__(x, y, (239, 87, 235))
        self.add_blocks()

    def add_blocks(self):

        b1 = Block(self.x-blocksize, self.y, blocksize, self.color)
        b2 = Block(self.x, self.y, blocksize, self.color)
        b3 = Block(self.x+blocksize, self.y, blocksize, self.color)
        b4 = Block(self.x, self.y-blocksize, blocksize, self.color)
        b5 = Block(self.x, self.y-2*blocksize, blocksize, self.color)
        b6 = Block(self.x, self.y-3*blocksize, blocksize, self.color)

        self.blocks = [b1, b2, b3, b4, b5, b6]
        self.angle_block = b2
        self.left_blocks = [b1]
        self.right_blocks = [b3]
        self.up_blocks = [b4, b5, b6]




class Gamefloor:

    def __init__(self, x, y, width, height, color):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x+self.width, self.y))
        pygame.draw.line(screen, self.color, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height))
        pygame.draw.line(screen, self.color, (self.x+self.width, self.y+self.height), (self.x, self.y+self.height))
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x, self.y+self.height))


"""
defining all blcoks variable
"""
all_blocks = [Long, Cube, Stairs, Corner]

def give_random_block_at_random_location():
    """
    gives back a random block inside gamefloor to play
    """
    penice_gotten = random.randrange(penice_chance)
    random_x = random.choice(all_choice_x)
    random_block = (random.choice(all_blocks) if not (penice_gotten==1) else Penice)

    #making block at random location
    back_block = random_block(random_x, gamefloor.y)
    back_block.sety(back_block.y+back_block.angle_block.y-back_block.find_highest().y)
    return back_block



class Fall_Regulator:

    """
    class for regulating the fall
    """
    def __init__(self, fat):
        self.falltime = fat
        self.last = time.perf_counter()
        self.curr = time.perf_counter()

    def can_fall(self):

        self.curr = time.perf_counter()
        if self.curr-self.last >= self.falltime:
            self.last = self.curr
            return True
        else:
            return False

class MoveRegulator(Fall_Regulator):

    def __init__(self, movt):
        super().__init__(movt)

    def can_move(self):
        return super().can_fall()


def hits(object, liste, x_mod=0, y_mod=0):
    back = False
    escape = False
    for lowest in object.blocks:
        for el in liste:
            for x in el.blocks:
                """
                low_x, low_y = lowest.x, lowest.y
                statement_one = (low_x >= x.x and low_x <= x.x+blocksize)
                statement_two = (low_x+blocksize >= x.x and low_x+blocksize <= x.x+blocksize)
                if low_y+blocksize >= x.y and (statement_one or statement_two):
                    back = True
                    escape = True
                    break
                """
                save_x, save_y = lowest.hitbox.x, lowest.hitbox.y
                lowest.hitbox.x = save_x+x_mod
                lowest.hitbox.y = save_y+y_mod
                if x.hitbox.is_colliding(lowest):
                    lowest.hitbox.x = save_x
                    lowest.hitbox.y = save_y
                    escape = True
                    back = True
                    break
                lowest.hitbox.x = save_x
                lowest.hitbox.y = save_y
        if escape:
            break

    return back

def check_is_ceiling(liste):
    back = False
    for el in liste:
        if el.find_highest().y <= gamefloor_y:
            back = True
    return back





"""
Making all objects
"""

gamefloor = Gamefloor(gamefloor_x, gamefloor_y, gamefloor_width, gamefloor_height, gamefloor_color)

rotreg = RotationRegulator(time_between_rotate)
fallreg = Fall_Regulator(falltime)
movereg = MoveRegulator(movetime)

ground_objects = []
current_object = None



def redraw():
    screen.fill((0, 0, 0))
    gamefloor.draw(screen)
    for el in ground_objects:
        el.draw(screen)
    if current_object is not None:
        current_object.draw(screen)
    pygame.display.flip()


while not ende:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ende = True

    pressed = pygame.key.get_pressed()


    if current_object is not None:

        lowest = current_object.find_lowest()
        hitting = hits(current_object, ground_objects)
        if lowest.y+blocksize >=gamefloor_y+gamefloor_height or hitting:
            ground_objects.append(current_object)
            current_object = None


        if current_object is not None:

            if rotreg.can_rotate():
                if pressed[pygame.K_a]:
                    current_object.rotate_left(gamefloor)

                if pressed[pygame.K_d]:
                    current_object.rotate_right(gamefloor)

            if fallreg.can_fall():
                current_object.move_up(fallspeed, gamefloor)


            if movereg.can_move():
                if pressed[pygame.K_RIGHT]:
                    if not hits(current_object, ground_objects, movespeed):
                        current_object.move_right(movespeed, gamefloor)
                    else:
                        gorund_objects.append(current_object)
                        current_object = None

                elif pressed[pygame.K_LEFT]:
                    if not hits(current_object, ground_objects, -movespeed):
                        current_object.move_right(-movespeed, gamefloor)
                    else:
                        ground_objects.append(current_object)
                        current_object = None
    else:
        current_object = give_random_block_at_random_location()

    if pressed[pygame.K_p]:
        ende = True

    ende = check_is_ceiling(ground_objects)




    redraw()

pygame.quit()
