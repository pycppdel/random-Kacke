"""
simulation of the reaction diffusion
"""
import pygame
import sys
import re
import random

pygame.init()


"""
dictionary with all parameters from conf
"""
parameters = {"width": None,
              "height": None,
               "fps": None,
               "background_color": None,
               "A_color": None,
               "B_color": None,
               "Cellsize": None,
               #Math stuff
               "diffusion_rate_a": None,
               "diffusion_rate_b": None,
               "feedrate": None,
               "killrate": None,
               "timedelta": None

             }

"""
loading conf
"""

#string for finding variables. Name needs to be added
loadstring = r"\s*=\s*([\(\)\[\],A-Za-z0-9_ \.]+)"
#making search strings
search_strings = [r" *("+el+r")"+loadstring for el in parameters]

with open("rd.conf", "r") as rd:
    #reading per line
    for el in rd.readlines():
        #checking for width and height
        for s in search_strings:
            found = re.search(s, el)
            if found:
                parameters[found.groups()[0]] = eval(found.groups()[1])


"""
All parameters loaded
"""
#checking for all
for el in parameters.values():
    if el is None:
        raise ValueError("not all values are set")


"""
setting global variables
"""
width, height = parameters["width"], parameters["height"]
#making screen
screen = pygame.display.set_mode((width, height))


#fps and clock
fps = parameters["fps"]

clock = pygame.time.Clock()

#end variable
ende = False

#colors
a_color = parameters["A_color"]
b_color = parameters["B_color"]

background_color = parameters["background_color"]

#size for cells
cellsize = parameters["Cellsize"]



"""
class for colored cell on screen
"""
class Cell:

    def __init__(self, x, y, a, b):
        """
        A and B proportions
        """
        self.x, self.y = x, y

        #cellsize
        self.size = cellsize
        #a and b prop
        self.a_proportion = a
        self.b_proportion = b


    def draw(self, screen):
        """
        draws on screen
        """
        #differential color
        diff_color = []
        for t in range(3):
            diff_color.append(((abs(self.a_proportion*a_color[t]))+(abs(self.b_proportion*b_color[t]))))
        diff_color = tuple(diff_color)
        pygame.draw.rect(screen, diff_color, (self.x,self.y, self.size, self.size))

"""
making cells inhabit the world
"""
#container for all cells
cells = {}
def cell_inhabit():
    """
    generates all cells
    """
    for a in range(height//cellsize):
        for b in range(width//cellsize):

            rate = (1, 0)
            cells[(b, a)] = Cell(cellsize*b, cellsize*a, *rate)

#calling
cell_inhabit()

cells[(width//cellsize//2, height//cellsize//2)].a_proportion = 0
cells[(width//cellsize//2, height//cellsize//2)].b_proportion = 1
cells[(width//cellsize//2-1, height//cellsize//2)].a_proportion = 0
cells[(width//cellsize//2-1, height//cellsize//2)].b_proportion = 1

"""
setting math
"""
diffusion_rate_a = parameters["diffusion_rate_a"]
diffusion_rate_b = parameters["diffusion_rate_b"]
feedrate = parameters["feedrate"]
killrate = parameters["killrate"]
timedelta = parameters["timedelta"]

def get_difference(coords):
    """
    gives back a and b average between neighbouring cells
    """
    a_sum = 0
    b_sum = 0

    cells_listed = 0

    dig_weight = 0.05
    next_weight = 0.2
    center_weight = -1

    if coords[0] == 0 or coords[0] == width//cellsize-1:
        return
    if coords[1] == 0 or coords[1] == height//cellsize-1:
        return




    try:
        a_sum += dig_weight*cells[(coords[0]-1, coords[1]-1)].a_proportion
    except:
        pass
    try:
        a_sum += next_weight*cells[(coords[0], coords[1]-1)].a_proportion
    except:
        pass
    try:
        a_sum += dig_weight*cells[(coords[0]+1, coords[1]-1)].a_proportion
    except:
        pass
    try:
        a_sum += next_weight*cells[(coords[0]-1, coords[1])].a_proportion
    except:
        pass
    try:
        a_sum += center_weight*cells[(coords[0], coords[1])].a_proportion
    except:
        pass
    try:
        a_sum += next_weight*cells[(coords[0]+1, coords[1])].a_proportion
    except:
        pass

    try:
        a_sum += dig_weight*cells[(coords[0]-1, coords[1]+1)].a_proportion
    except:
        pass

    try:
        a_sum += next_weight*cells[(coords[0], coords[1]+1)].a_proportion
    except:
        pass

    try:
        a_sum += dig_weight*cells[(coords[0]+1, coords[1]+1)].a_proportion
    except:
        pass

    """
    Part B
    """

    try:
        b_sum += dig_weight*cells[(coords[0]-1, coords[1]-1)].b_proportion
    except:
        pass
    try:
        b_sum += next_weight*cells[(coords[0], coords[1]-1)].b_proportion
    except:
        pass
    try:
        b_sum += dig_weight*cells[(coords[0]+1, coords[1]-1)].b_proportion
    except:
        pass
    try:
        b_sum += next_weight*cells[(coords[0]-1, coords[1])].b_proportion
    except:
        pass
    try:
        b_sum += center_weight*cells[(coords[0], coords[1])].b_proportion
    except:
        pass
    try:
        b_sum += next_weight*cells[(coords[0]+1, coords[1])].b_proportion
    except:
        pass

    try:
        b_sum += dig_weight*cells[(coords[0]-1, coords[1]+1)].b_proportion
    except:
        pass

    try:
        b_sum += next_weight*cells[(coords[0], coords[1]+1)].b_proportion
    except:
        pass

    try:
        b_sum += dig_weight*cells[(coords[0]+1, coords[1]+1)].b_proportion
    except:
        pass


    return (a_sum, b_sum)

def change_cells():
    global cells
    """
    changes all cells
    """
    cellcopy = {el: Cell(cells[el].x, cells[el].y, cells[el].a_proportion, cells[el].b_proportion) for el in cells}
    for el in cells:
        """
        starting per cell
        """
        cell = cellcopy[el]

        if el[0] == 0 or el[0] == width//cellsize-1:
            continue
        if el[1] == 0 or el[1] == height//cellsize-1:
            continue

        answer = get_difference(el)

        if answer is None:
            continue
        a_average, b_average = answer



        #cell.a_proportion =cell.a_proportion+((diffusion_rate_a*a_average*cell.a_proportion)-(cell.a_proportion*(cell.b_proportion**2))\
        #+(feedrate*(1-cell.a_proportion)))*timedelta
        #cell.b_proportion = cell.b_proportion+((diffusion_rate_b*b_average*cell.b_proportion)+(cell.a_proportion*(cell.b_proportion**2))\
        #-((killrate+feedrate)*cell.b_proportion))*timedelta
        cell.a_proportion = (cell.a_proportion)+((diffusion_rate_a*a_average*cell.a_proportion)\
        -(cell.a_proportion*(cell.b_proportion**2))+(feedrate*(1-cell.a_proportion)))*timedelta
        cell.b_proportion = (cell.b_proportion)+((diffusion_rate_b*b_average*cell.b_proportion)\
        +(cell.a_proportion*(cell.b_proportion**2))-((killrate+feedrate)*cell.b_proportion))*timedelta
        """
        Checking
        """

        #checking if higher or lower
        if cell.a_proportion > 1:
            cell.a_proportion = 1
        elif cell.a_proportion < 0:
            cell.a_proportion = 0
        #same for b
        if cell.b_proportion > 1:
            cell.b_proportion = 1
        elif cell.b_proportion < 0:
            cell.b_proportion = 0

    cells = cellcopy

def redraw():
    screen.fill(background_color)
    """
    drawing all cells
    """
    for el in cells.values():
        el.draw(screen)
    pygame.display.flip()

while not ende:

    clock.tick(fps)

    #event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ende = True

    #changing cells
    change_cells()
    #redrawing
    redraw()


pygame.quit()
