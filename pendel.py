import pygame
import math

pygame.init()

width, height = 800, 800

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Pendel")

ende = False

fps = 60

clock = pygame.time.Clock()

class Pendel:

    def __init__(self, x, y, length, mass):

        #setting origing
        self.x, self.y = x, y
        self.length, self.mass = length, mass

        self.theta = 0

        self.direction = "r"

        self.set_coords()
        self.set_side_vel(4)


    def set_side_vel(self, val):
        self.theta = self.change_to_deg(10*val)
        self.side_vel = 0
        self.save_side_vel = val

    def change_to_deg(self, val):
        return (math.pi*2/360*val)

    def set_coords(self):
        self.bx, self.by = math.sin(self.theta)*self.length, math.cos(self.theta)*self.length

    def update_side_vel(self):
        pullback = self.bx
        pullback = -pullback
        pullback /= 2
        percent = pullback/(math.pi*self.length)
        self.side_vel += self.save_side_vel*percent/2
        self.theta += self.change_to_deg(self.side_vel)



    def update(self):
        self.update_side_vel()
        self.set_coords()

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.bx+self.x, self.by+self.y))
        pygame.draw.circle(screen, (0, 0, 0), (self.bx+self.x, self.by+self.y), 8)

p = Pendel(width//2, height//2, 300, 2)
def redraw():
    screen.fill((255, 255, 255))
    p.draw(screen)
    pygame.display.flip()

clicked = False

if __name__ == "__main__":
    while not ende:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ende = True

        pressed = pygame.mouse.get_pressed()

        m_x, m_y = pygame.mouse.get_pos()

        p.update()


        redraw()


    pygame.quit()
