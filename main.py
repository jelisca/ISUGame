# ICS4U1 ISU
# Jelisa Cao


# the pygame manual was extensively used: https://www.pygame.org/docs/
import pygame
import sys
import time
import random

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
        if self.velocity > 0:
            self.pos = self.rect.center = LEFT
        else:
            self.pos = self.rect.center = RIGHT

    def can_deploy(self):
        if time.time() - self.gst >= self.delay:
            return True
        else:
            return False

    def move(self):
        self.rect.move_ip([self.velocity, 0])
        self.pos = self.rect.center
        SCREEN.blit(self.image, self.rect)

    def border_check(self):
        if self.velocity < 0:
            if self.pos[0] <= LENGTH/2 + WHEEL_RADIUS * self.velocity/abs(self.velocity):
                return False
            else:
                return True
        elif self.velocity > 0:
            if self.pos[0] >= LENGTH/2 + WHEEL_RADIUS * self.velocity/abs(self.velocity):
                return False
            else:
                return True

    def key_is_pressed(self):
        key_state = pygame.key.get_pressed()
        if self.velocity > 0:
            if key_state[pygame.K_a]:
                return True
            else:
                return False
        else:
            if key_state[pygame.K_s]:
                return True
            else:
                return False

    def kill(self):
        # check ball velocity to determine key to use for killing
        # after killing, reset self.gst
        if self.velocity > 0:
            self.rect.center = LEFT
            self.delay = random.randint(0, 3)
            self.gst = time.time()
        else:
            self.rect.center = RIGHT
            self.delay = random.randint(0, 3)
            self.gst = time.time()

    def update(self):
        # after killed OR border crossed, move note back to original position, and set with new delay
        if self.border_check() and not self.key_is_pressed():
            self.move()
        else:
            self.kill()


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


#  class NotesQueue:

#      def __init__(self):
#          self.notes_queue = []
#          #  self.start_time  = time.time()

#      def put_note(self, note):
#          #  note = ArrowNote(default_note_attrs, self.start_time)
#          if note.can_deploy():
#              self.notes_queue.append(note)

#      def remove_note(self):
#          self.notes_queue.pop(0)

#      def move_notes(self):
#          print(len(self.notes_queue))
#          for note in self.notes_queue:
#              note.move()


def main():
    #starting time of game
    start_time = time.time()

    #  nq = NotesQueue()
    #  note_gen = generate_notes(10000, start_time)

    #  note = ArrowNote(default_note_attrs, start_time)
    #  nq.put_note(note)
    #  default_note_attrs.update({'velocity': 1, 'delay': 2, 'color': 'green'})
    #  note = ArrowNote(default_note_attrs, start_time)

    left_note  = ArrowNote({'velocity': 10, 'radius': WHEEL_RADIUS/3, 'color': 'red', 'delay': random.randint(0, 3)}, start_time)
    right_note = ArrowNote({'velocity': -10, 'radius': WHEEL_RADIUS/3, 'color': 'green', 'delay': random.randint(0, 3)}, start_time)

    # initializes display mode
    pygame.init()

    target = PlayerWheel()

    # game loop
    while True:
        #  note = yield next(note_gen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('white')
        target.update()

        if left_note.can_deploy():
            # left_note.move()
            left_note.update()
        if right_note.can_deploy():
            # right_note.move()
            right_note.update()
        #  nq.move_notes()


        pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    main()
