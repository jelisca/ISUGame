# ICS4U1 ISU
# Jelisa Cao


# the pygame manual was extensively used: https://www.pygame.org/docs/
import pygame
import sys
import time
import random

# initializes display mode
pygame.init()

LENGTH = 2000
HEIGHT = 1000
WHEEL_RADIUS = 210

LEFT = [0, HEIGHT/2]
RIGHT = [LENGTH, HEIGHT/2]

FPS = 40
FramePerSecond = pygame.time.Clock()

SCREEN = pygame.display.set_mode([LENGTH, HEIGHT])
pygame.display.set_caption("Play")
score_font = pygame.font.SysFont("arial", 40)
go_font = pygame.font.SysFont("arial", 200)


class ArrowNote(pygame.sprite.Sprite):

    def __init__(self, note_attrs):
        self.velocity = note_attrs['velocity']
        self.radius   = note_attrs['radius']
        self.color    = note_attrs['color']
        self.delay    = note_attrs['delay']
        self.gst      = time.time()
        self.score    = 0
        self.miss     = False

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

    def add_score(self):
        if self.pos[0] > LENGTH/2 - WHEEL_RADIUS and self.pos[0] < LENGTH/2 + WHEEL_RADIUS:
            if self.pos[0] > LENGTH/2 - WHEEL_RADIUS/3 and self.pos[0] < LENGTH/2 + WHEEL_RADIUS/3:
                self.score += 100
            else:
                self.score += 50

    def speed_rate(self, gametime):
        increase_by = (time.time() - gametime) / 50000
        self.velocity *= (1 + increase_by)

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
        if self.velocity > 0:
            if self.pos[0] >= LENGTH/2 + WHEEL_RADIUS:
                return False
            else:
                return True
        else:
            if self.pos[0] <= LENGTH / 2 - WHEEL_RADIUS:
                return False
            else:
                return True

    def miss_check(self):
        if not self.border_check():
            self.miss = True
        elif self.velocity > 0:
            if self.pos[0] <= LENGTH / 2 - WHEEL_RADIUS:
                self.miss = True
        elif self.velocity < 0:
            if self.pos[0] >= LENGTH/2 + WHEEL_RADIUS:
                self.miss = True

    def key_is_pressed(self):
        key_state = pygame.key.get_pressed()
        if self.velocity > 0:
            if key_state[pygame.K_a] or key_state[pygame.K_LEFT]:
                return True
            else:
                return False
        else:
            if key_state[pygame.K_d] or key_state[pygame.K_RIGHT]:
                return True
            else:
                return False

    def kill(self):
        # check ball velocity to determine key to use for killing
        # after killing, reset self.gst'
        self.add_score()
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
            self.miss_check()
            self.kill()


class PlayerWheel(pygame.sprite.Sprite):

    def __init__(self):
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


def main():
    game_time = time.time()

    left_note  = ArrowNote({'velocity': 10, 'radius': WHEEL_RADIUS/3, 'color': 'red', 'delay': random.randint(0, 3)})
    right_note = ArrowNote({'velocity': -10, 'radius': WHEEL_RADIUS/3, 'color': 'green', 'delay': random.randint(0, 3)})

    target = PlayerWheel()

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        print([left_note.miss, right_note.miss])

        if not left_note.miss and not right_note.miss:
            score_display = score_font.render('Score: ' + str(left_note.score + right_note.score), True, 'white', 'black')
            score_rect = score_display.get_rect()
            score_rect.center = (LENGTH / 2, HEIGHT / 8)

            SCREEN.fill('white')
            SCREEN.blit(score_display, score_rect)
            target.update()

            if left_note.can_deploy():
                left_note.update()
                left_note.speed_rate(game_time)

            if right_note.can_deploy():
                right_note.update()
                right_note.speed_rate(game_time)
        else:
            game_over = go_font.render('GAMEOVER', True, 'white', 'black')
            game_over_display = game_over.get_rect()
            game_over_display.center = (LENGTH / 2, HEIGHT / 2)
            SCREEN.blit(game_over, game_over_display)

        pygame.display.update()

        FramePerSecond.tick(FPS)



if __name__ == '__main__':
    main()
