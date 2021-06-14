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
HEIGHT = 1500
WHEEL_RADIUS = 210

LEFT = [0, HEIGHT/2]
RIGHT = [LENGTH, HEIGHT/2]
TOP = [LENGTH/2, 0]
BOTTOM = [LENGTH/2, HEIGHT]

FPS = 40
FramePerSecond = pygame.time.Clock()

SCREEN = pygame.display.set_mode([LENGTH, HEIGHT])

# TODO: Fix speed up rate resetting

class Note(pygame.sprite.Sprite):

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
        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                self.pos = self.rect.center = LEFT
            else:
                self.pos = self.rect.center = RIGHT
        else:
            if self.velocity[1] > 0:
                self.pos = self.rect.center = TOP
            else:
                self.pos = self.rect.center = BOTTOM

    def add_score(self):
        if self.velocity[0] != 0:
            if self.pos[0] > LENGTH/2 - WHEEL_RADIUS and self.pos[0] < LENGTH/2 + WHEEL_RADIUS:
                if self.pos[0] > LENGTH/2 - WHEEL_RADIUS/3 and self.pos[0] < LENGTH/2 + WHEEL_RADIUS/3:
                    self.score += 100
                else:
                    self.score += 50
        else:
            if self.pos[1] < HEIGHT/2 + WHEEL_RADIUS and self.pos[1] > HEIGHT/2 - WHEEL_RADIUS:
                if self.pos[1] < HEIGHT/2 + WHEEL_RADIUS/3 and self.pos[1] > HEIGHT - WHEEL_RADIUS/3:
                    self.score += 100
                else:
                    self.score += 50

    def speed_rate(self, gametime):
        increase_by = (time.time() - gametime) / 50000
        if self.velocity[0] != 0:
            self.velocity[0] *= 1 + increase_by
        else:
            self.velocity[1] *= 1 + increase_by

    def can_deploy(self):
        if time.time() - self.gst >= self.delay:
            return True
        else:
            return False

    def move(self):
        self.rect.move_ip(self.velocity)
        self.pos = self.rect.center
        SCREEN.blit(self.image, self.rect)

    def border_check(self):
        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                if self.pos[0] >= LENGTH / 2 + WHEEL_RADIUS:
                    return False
                else:
                    return True
            else:
                if self.pos[0] <= LENGTH / 2 - WHEEL_RADIUS:
                    return False
                else:
                    return True
        else:
            if self.velocity[1] > 0:
                if self.pos[1] >= HEIGHT / 2 + WHEEL_RADIUS:
                    return False
                else:
                    return True
            else:
                if self.pos[1] <= HEIGHT / 2 - WHEEL_RADIUS:
                    return False
                else:
                    return True

    def miss_check(self):
        if not self.border_check():
            self.miss = True

        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                if self.pos[0] <= LENGTH / 2 - WHEEL_RADIUS:
                    self.miss = True
            else:
                if self.pos[0] >= LENGTH/2 + WHEEL_RADIUS:
                    self.miss = True
        else:
            if self.velocity[1] > 0:
                if self.pos[1] <= HEIGHT / 2 - WHEEL_RADIUS:
                    self.miss = True
            else:
                if self.pos[1] >= HEIGHT / 2 + WHEEL_RADIUS:
                    self.miss = True

    def key_is_pressed(self):
        key_state = pygame.key.get_pressed()
        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                if key_state[pygame.K_a] or key_state[pygame.K_LEFT]:
                    return True
                else:
                    return False
            else:
                if key_state[pygame.K_d] or key_state[pygame.K_RIGHT]:
                    return True
                else:
                    return False
        else:
            if self.velocity[1] > 0:
                if key_state[pygame.K_w] or key_state[pygame.K_UP]:
                    return True
                else:
                    return False
            else:
                if key_state[pygame.K_s] or key_state[pygame.K_DOWN]:
                    return True
                else:
                    return False

    def kill(self):
        # check ball velocity to determine key to use for killing
        # after killing, reset self.gst'
        self.add_score()
        if self.velocity[0] != 0:
            if self.velocity[0] > 0:
                self.rect.center = LEFT
                self.delay = random.randint(0, 3)
                self.gst = time.time()
            else:
                self.rect.center = RIGHT
                self.delay = random.randint(0, 3)
                self.gst = time.time()
        else:
            if self.velocity[1] > 0:
                self.rect.center = TOP
                self.delay = random.randint(0, 3)
                self.gst = time.time()
            else:
                self.rect.center = BOTTOM
                self.delay = random.randint(0, 3)
                self.gst = time.time()

    def update(self):
        # after killed OR border crossed, move note back to original position, and set with new delay
        if self.border_check() and not self.key_is_pressed():
            self.move()
        else:
            self.miss_check()
            self.kill()

    def reset(self):
        self.kill()
        self.score = 0
        self.miss = False


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


class MenuButton():
    pressed = False

    def __init__(self, button_attrs):
        self.position = button_attrs['pos']
        self.text = button_attrs['txt']
        self.color = button_attrs['color']

        self.font = pygame.font.SysFont("arial", 100)

        self.button_text = self.font.render(self.text, True, 'white', self.color)
        self.button_display = self.button_text.get_rect()
        self.button_display.center = self.position

    def is_clicked(self):
        if not self.pressed:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.position[0] - LENGTH/2 < x < self.position[0] + LENGTH/2 and self.position[1] - 30 < y < self.position[1] + 30:
                    self.pressed = True

    def update(self):
        if not self.pressed:
            SCREEN.blit(self.button_text, self.button_display)

def main():
    game_time = time.time()

    start_button = MenuButton({'pos': [LENGTH/2, HEIGHT/2], 'txt': 'START', 'color': 'black'})
    howto_button = MenuButton({'pos': [LENGTH/2, HEIGHT/4], 'txt': 'HOW TO PLAY', 'color': 'blue'})
    seldiff_button = MenuButton({'pos': [LENGTH/2, HEIGHT * 3/4], 'txt': 'SELECT DIFFICULTY', 'color': 'black'})

    left_note  = Note({'velocity': [10, 0], 'radius': WHEEL_RADIUS/3, 'color': 'red', 'delay': random.randint(0, 3)})
    right_note = Note({'velocity': [-10, 0], 'radius': WHEEL_RADIUS/3, 'color': 'green', 'delay': random.randint(0, 3)})
    top_note = Note({'velocity': [0, 10], 'radius': WHEEL_RADIUS/3, 'color': 'purple', 'delay': random.randint(0, 3)})
    bottom_note = Note({'velocity': [0, -10], 'radius': WHEEL_RADIUS/3, 'color': 'orange', 'delay': random.randint(0, 3)})

    difficulty = 0

    target = PlayerWheel()

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('white')

        if start_button.pressed:

            if not left_note.miss and not right_note.miss and not top_note.miss and not bottom_note.miss:
                pygame.display.set_caption("Playing")

                score = str(left_note.score + right_note.score + top_note.score + bottom_note.score)

                score_font = pygame.font.SysFont("arial", 40)
                score_display = score_font.render('Score: ' + score, True, 'white', 'black')
                score_rect = score_display.get_rect()
                score_rect.center = (LENGTH / 2, HEIGHT / 8)
                SCREEN.blit(score_display, score_rect)

                target.update()

                if left_note.can_deploy():
                    left_note.update()
                    left_note.speed_rate(game_time)

                if right_note.can_deploy():
                    right_note.update()
                    right_note.speed_rate(game_time)

                if difficulty >= 1:
                    if top_note.can_deploy():
                        top_note.update()
                        top_note.speed_rate(game_time)

                if difficulty >= 2:
                    if bottom_note.can_deploy():
                        bottom_note.update()
                        bottom_note.speed_rate(game_time)

            else:
                pygame.display.set_caption("Gameover")

                go_font = pygame.font.SysFont("arial", 200)
                game_over = go_font.render('GAMEOVER', True, 'white', 'black')
                game_over_display = game_over.get_rect()
                game_over_display.center = (LENGTH / 2, HEIGHT / 2)
                SCREEN.blit(game_over, game_over_display)

                SCREEN.blit(score_display, score_rect)

                back_button = MenuButton({'pos': [LENGTH / 2, HEIGHT * 2/ 3], 'txt': 'BACK', 'color': 'RED'})
                back_button.update()
                back_button.is_clicked()

                if back_button.pressed:
                    start_button.pressed = False
                    howto_button.pressed = False

                    left_note.reset()
                    right_note.reset()
                    top_note.reset()
                    bottom_note.reset()

                    game_time = time.time()

        elif howto_button.pressed:
            howto_welcome = 'Welcome!'
            howto_about = 'This game is a simple, reaction-based game based on circles.'
            howto_goal = 'The goal is to make approaching notes disappear in the central target.'
            howto_controls = 'To make notes disappear, use the WASD or arrow keys to the corresponding side the note comes from!'
            howto_score = 'Making notes disappear closer to the center of the target will award more points to your score.'
            howto_gameover = 'Make sure to not over or under estimate the note! If the note disappears before or after the target it will be a game over.'
            howto_speed = 'The longer you play a single game, the faster the notes will move.'
            howto_prompt = 'Try it out!'

            howto_font = pygame.font.SysFont("arial", 35)

            def show_text(text, h):
                howto_display = howto_font.render(text, True, 'black', 'white')
                howto_rect = howto_display.get_rect()
                howto_rect.center = (LENGTH / 2, h)
                SCREEN.blit(howto_display, howto_rect)

            show_text(howto_welcome, 100)
            show_text(howto_about, 200)
            show_text(howto_goal, 300)
            show_text(howto_controls, 400)
            show_text(howto_score, 600)
            show_text(howto_gameover, 700)
            show_text(howto_speed, 800)
            show_text(howto_prompt, 900)

            back_button = MenuButton({'pos': [LENGTH / 2, 1000], 'txt': 'BACK', 'color': 'black'})
            back_button.update()
            back_button.is_clicked()

            if back_button.pressed:
                howto_button.pressed = False

        elif seldiff_button.pressed:
            pygame.display.set_caption("Selecting Difficulty")

            easy_button = MenuButton({'pos': [LENGTH / 2, 400], 'txt': 'EASY', 'color': 'green'})
            med_button = MenuButton({'pos': [LENGTH / 2, 600], 'txt': 'MEDIUM', 'color': 'orange'})
            hard_button = MenuButton({'pos': [LENGTH /2, 800], 'txt': 'HARD', 'color': 'red'})

            easy_button.update()
            easy_button.is_clicked()
            if easy_button.pressed:
                pygame.display.set_caption("Easy Mode Selected")
                difficulty = 0

            med_button.update()
            med_button.is_clicked()
            if med_button.pressed:
                pygame.display.set_caption("Medium Mode Selected")
                difficulty = 1

            hard_button.update()
            hard_button.is_clicked()
            if hard_button.pressed:
                pygame.display.set_caption("Hard Mode Selected")
                difficulty = 2

            back_button = MenuButton({'pos': [LENGTH / 2, HEIGHT / 8], 'txt': 'BACK', 'color': 'black'})
            back_button.update()
            back_button.is_clicked()

            font = pygame.font.SysFont("arial", 35)

            howto_display = font.render('Increasing difficulty will increase the number of notes at a time.', True, 'black', 'white')
            howto_rect = howto_display.get_rect()
            howto_rect.center = (LENGTH / 2, 1300)
            SCREEN.blit(howto_display, howto_rect)

            if back_button.pressed:
                easy_button.pressed = False
                med_button.pressed = False
                hard_button.pressed = False

                seldiff_button.pressed = False

        else:
            pygame.display.set_caption("Main Menu")

            start_button.update()
            start_button.is_clicked()

            howto_button.update()
            howto_button.is_clicked()

            seldiff_button.update()
            seldiff_button.is_clicked()

        pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    main()
