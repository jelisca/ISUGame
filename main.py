# ICS4U1 ISU
# Jelisa Cao


# the pygame manual was extensively used: https://www.pygame.org/docs/
import pygame
import sys
import time

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


class ArrowNote(pygame.sprite.Sprite):

    def __init__(self, note_attrs, game_start_time):
        self.velocity = note_attrs['velocity']
        self.radius   = note_attrs['radius']
        self.color    = note_attrs['color']
        self.delay    = note_attrs['delay']
        self.gst      = game_start_time

        super().__init__()

        self.image = pygame.Surface([self.radius*2, self.radius*2])
        self.rect  = self.image.get_rect()
        self.image.fill('white')
        self.image.set_colorkey('white')
        pygame.draw.circle(self.image, self.color, self.rect.center, self.radius)
        self.pos   = self.rect.center

    def can_deploy(self):
        if time.time() - self.gst >= self.delay:
            return True
        else:
            return False

    def move(self):
        self.rect.move_ip([self.velocity, 0])
        self.pos = self.rect.center
        SCREEN.blit(self.image, self.rect)
        #  print(self.pos)


class Blah:

    miss = False
    lock = True
    killed = False

    def ___init__(self, vel, rad, colour, start, delay_time):
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

    def key_check(self):
        if self.miss == False:
            if self.lock == False:
                events = pygame.event.get()
                for event in events:
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


default_note_attrs = {'velocity': 10, 'radius': WHEEL_RADIUS/3, 'color': 'red', 'delay': 0}

class NotesQueue:

    def __init__(self):
        self.notes_queue = []
        #  self.start_time  = time.time()

    def put_note(self, note):
        #  note = ArrowNote(default_note_attrs, self.start_time)
        if note.can_deploy():
            self.notes_queue.append(note)

    def get_note(self):
        pass

    def move_notes(self):
        print(len(self.notes_queue))
        for note in self.notes_queue:
            note.move()


def main():
    #starting time of game
    start_time = time.time()

    nq = NotesQueue()
    note = ArrowNote(default_note_attrs, start_time)
    nq.put_note(note)
    default_note_attrs.update({'velocity': 2, 'delay': 3, 'color': 'green'})
    note = ArrowNote(default_note_attrs, start_time)

    # initializes display mode
    pygame.init()

    target = PlayerWheel()

    # game loop
    while True:

        nq.put_note(note)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('white')

        nq.move_notes()
        target.update()

        pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    main()
