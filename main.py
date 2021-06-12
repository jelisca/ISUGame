# ICS4U1 ISU
# Jelisa Cao


# the pygame manual was extensively used: https://www.pygame.org/docs/
import pygame
import sys
import time
from pygame.locals import *

LENGTH = 2000
HEIGHT = 1000
WHEEL_RADIUS = 210

LEFT = [0, HEIGHT/2]
RIGHT = [LENGTH, HEIGHT/2]

FPS = 40
FramePerSecond = pygame.time.Clock()

SCREEN = pygame.display.set_mode([LENGTH, HEIGHT])
pygame.display.set_caption("Singleplayer Taiko DDR")

MULTIPLAYER = False
DIFF_SEL = 0
SCORE = 0

#TODO:colour selection for each player
#TODO:Aproject spawning for both players
#TODO: Working Score System and Labeling


class AproachingObj(pygame.sprite.Sprite):

    miss = False
    lock = True
    killed = False

    def __init__(self, vel, rad, colour, start, delay_time):
        self.vel = vel
        self.rad = rad
        self.colour = colour
        self.start = start
        self.delay_time = delay_time

        #https://www.101computing.net/creating-sprites-using-pygame/
        #referenced for sprite creation
        super().__init__()

        self.image = pygame.Surface([self.rad*2, self.rad*2])
        self.rect = self.image.get_rect()
        self.image.fill('white')
        self.image.set_colorkey('white')
        pygame.draw.circle(self.image, self.colour, self.rect.center, self.rad)
        self.pos = self.rect.center = self.start

    def move(self):
        self.rect.move_ip([self.vel, 0])
        self.pos = self.rect.center
        SCREEN.blit(self.image, self.rect)

    def deploy_check(self, starttime):
        tick = time.time()
        if tick - starttime >= self.delay_time:
            return True
        else:
            return False

    def key_check(self):
        if self.miss == False:
            if self.lock == False:
                events = pygame.event.get()
                for event in events:
                    #print(event[K_a], event[K_s])
                    if event.type == pygame.KEYDOWN:
                        print(self.colour)
                        print(self.killed)
                        if event.key == pygame.K_a or event.key == pygame.K_s:
                            self.miss = True
                            return False
                        else:
                            return True
                    else:
                        return True
            else:
                return True

    def border_check(self):
        if self.start == RIGHT:
            if self.pos[0] <= LENGTH/2 + WHEEL_RADIUS * self.vel/abs(self.vel):
                return False
            else:
                return True
        elif self.start == LEFT:
            if self.pos[0] >= LENGTH/2 + WHEEL_RADIUS * self.vel/abs(self.vel):
                return False
            else:
                return True

    def can_kill(self, starttime):
        if self.deploy_check(starttime) and self.lock is False:
            return True
        else:
            return False

    def update(self, starttime):
        if self.deploy_check(starttime) and not self.killed:
            if self.border_check() and not self.key_check():
                self.move()
            else:
                if self.can_kill(starttime):
                    print(f'{self.colour} is killed')
                    self.killed = True
                    self.kill()


class PlayerWheel(pygame.sprite.Sprite):

    def __init__(self):
        if MULTIPLAYER:
            pass
        else:
            self.pos = [LENGTH/2, HEIGHT/2]

        super().__init__()
        self.image = pygame.Surface([WHEEL_RADIUS * 2, WHEEL_RADIUS * 2])
        self.rect = self.image.get_rect()
        self.image.fill('white')
        self.image.set_colorkey('white')
        pygame.draw.circle(self.image, 'pink', self.rect.center, WHEEL_RADIUS)
        self.rect.center = self.pos

    def update(self):
        SCREEN.blit(self.image, self.rect)


def init_stream():
    song_ls = []

    p1_aprobj1 = AproachingObj(10, WHEEL_RADIUS / 3, 'red', LEFT, 0)
    p1_aprobj2 = AproachingObj(-10, WHEEL_RADIUS / 3, 'blue', RIGHT, 2)
    p1_aprobj3 = AproachingObj(10, WHEEL_RADIUS / 3, 'green', LEFT, 3)
    p1_aprobj4 = AproachingObj(10, WHEEL_RADIUS / 3, 'purple', LEFT, 5)
    p1_aprobj5 = AproachingObj(-10, WHEEL_RADIUS / 3, 'orange', RIGHT, 6)
    p1_aprobj6 = AproachingObj(-10, WHEEL_RADIUS / 3, 'grey', RIGHT, 6.5)

    song_ls = [p1_aprobj1, p1_aprobj2, p1_aprobj3, p1_aprobj4, p1_aprobj6]

    return song_ls


def generate_object(start_time, delay):
    if start_time - delay < 0:
        return AproachingObj(10, WHEEL_RADIUS / 3, 'red', LEFT, delay)




def play(starttime, tot_objects):

    for aprobject in tot_objects:
        index = tot_objects.index(aprobject)

        deployed_objs = sorted([ob for ob in tot_objects if ob.deploy_check(starttime) and not ob.killed], key=lambda x: x.delay_time)

        try:
            killable = min([(ob.colour, abs(ob.pos[0] - LENGTH / 2)) for ob in deployed_objs], key=lambda x: x[1])
            if aprobject.colour == killable[0]:
                aprobject.lock = False
        except ValueError:
            pass



        aprobject.update(starttime)

def main():
    #starting time of game
    start_time = time.time()

    # initializes display mode
    pygame.init()

    song_objects = init_stream()
    p1 = PlayerWheel()

    delays = range(10)
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('white')

        p1.update()
        play(start_time, song_objects)

        pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    main()
