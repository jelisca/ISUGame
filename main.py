# ICS4U1 ISU
# Jelisa Cao


# the pygame manual was extensively used: https://www.pygame.org/docs/
import pygame
import sys
import time
import random

# initializes display mode
pygame.init()

# global variables for object sizes
infoObject = pygame.display.Info()

LENGTH = infoObject.current_w
HEIGHT = infoObject.current_h
WHEEL_RADIUS = 210

SCREEN = pygame.display.set_mode([LENGTH, HEIGHT])

# global variables for note positions
LEFT = [0, HEIGHT/2]
RIGHT = [LENGTH, HEIGHT/2]
TOP = [LENGTH/2, 0]
BOTTOM = [LENGTH/2, HEIGHT]

# global variables for frame ticks
FPS = 40
FramePerSecond = pygame.time.Clock()


# class for note objects
class Note(pygame.sprite.Sprite):

    # initialize using a dictionary of the attributes
    def __init__(self, note_attrs):
        self.velocity = note_attrs['velocity']
        self.radius   = note_attrs['radius']
        self.color    = note_attrs['color']
        self.delay    = note_attrs['delay']
        self.gst      = time.time()
        self.score    = 0
        self.miss     = False

        # initializes the sprite
        super().__init__()

        # creates the sprite
        self.image = pygame.Surface([self.radius*2, self.radius*2])
        self.rect  = self.image.get_rect()
        self.image.fill('white')
        self.image.set_colorkey('white')
        pygame.draw.circle(self.image, self.color, self.rect.center, self.radius)

        # determines the starting position of the note by the velcity vector
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
        # rewards score based on how close the note is to the center of the target
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
        # increases velocity of the note by how much time has passed since the game started
        increase_by = (time.time() - gametime) / 50000
        if self.velocity[0] != 0:
            self.velocity[0] *= 1 + increase_by
        else:
            self.velocity[1] *= 1 + increase_by

    def can_deploy(self):
        # for the delay of the note
        if time.time() - self.gst >= self.delay:
            return True
        else:
            return False

    def move(self):
        # makes the note move by the velocity for a frame
        self.rect.move_ip(self.velocity)
        self.pos = self.rect.center
        SCREEN.blit(self.image, self.rect)

    def border_check(self):
        # checks if the note has passed a border depending on which side it starts on

        # for notes on the x axis
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
        # for notes on the y axis
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

    # checks if the player made a miss
    def miss_check(self):
        #missed when the note passes the target
        if not self.border_check():
            self.miss = True

        # missed when the note disappears outside the target
        elif self.velocity[0] != 0:
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

    # checks if a key is pressed
    def key_is_pressed(self):

        key_state = pygame.key.get_pressed()
        # checks the key for a specific side
        # x-axis notes
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
        # y-axis notes
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
        # after killing, reset self.gst
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

    # moves and checks for misses to disappear
    def update(self):
        # after killed OR border crossed, move note back to original position, and set with new delay
        if self.border_check() and not self.key_is_pressed():
            self.move()
        else:
            self.miss_check()
            self.kill()

    # reset note attrs for gameover
    def reset(self):
        self.miss = False
        self.kill()
        self.score = 0


# creates the central target
class PlayerWheel(pygame.sprite.Sprite):

    # initialize target
    def __init__(self):
        self.pos = [LENGTH/2, HEIGHT/2]

        super().__init__()
        self.image = pygame.Surface([WHEEL_RADIUS * 2, WHEEL_RADIUS * 2])
        self.rect = self.image.get_rect()
        self.image.fill('white')
        self.image.set_colorkey('white')
        pygame.draw.circle(self.image, 'pink', self.rect.center, WHEEL_RADIUS)
        self.rect.center = self.pos

    # shows target
    def update(self):
        SCREEN.blit(self.image, self.rect)


# class for menu buttons
class MenuButton():
    pressed = False

    # initializes menu button text
    def __init__(self, button_attrs):
        self.position = button_attrs['pos']
        self.text = button_attrs['txt']
        self.color = button_attrs['color']

        self.font = pygame.font.SysFont("arial", 100)

        self.button_text = self.font.render(self.text, True, 'white', self.color)
        self.button_display = self.button_text.get_rect()
        self.button_display.center = self.position

    # checks if the button is clicked
    def is_clicked(self):
        if not self.pressed:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.position[0] - LENGTH/2 < x < self.position[0] + LENGTH/2 and self.position[1] - 30 < y < self.position[1] + 30:
                    self.pressed = True

    # shows button
    def update(self):
        if not self.pressed:
            SCREEN.blit(self.button_text, self.button_display)


# default easy difficulty
difficulty = 0
diff = 'EASY'


# main function for gameplay
def main():
    global diff
    global difficulty

    # initializes and plays the music from the mp3 file
    pygame.mixer.init()
    pygame.mixer.music.load("Coconut_Mall.ogg")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # creates buttons for the main menu
    start_button = MenuButton({'pos': [LENGTH/2, HEIGHT/2], 'txt': 'START', 'color': 'black'})
    howto_button = MenuButton({'pos': [LENGTH/2, HEIGHT/4], 'txt': 'HOW TO PLAY', 'color': 'blue'})
    seldiff_button = MenuButton({'pos': [LENGTH/2, HEIGHT * 3/4], 'txt': 'SELECT DIFFICULTY', 'color': 'black'})

    # creating the notes; randomized delay
    left_note  = Note({'velocity': [10, 0], 'radius': WHEEL_RADIUS/3, 'color': 'red', 'delay': random.randint(0, 3)})
    right_note = Note({'velocity': [-10, 0], 'radius': WHEEL_RADIUS/3, 'color': 'green', 'delay': random.randint(0, 3)})
    top_note = Note({'velocity': [0, 10], 'radius': WHEEL_RADIUS/3, 'color': 'purple', 'delay': random.randint(0, 3)})
    bottom_note = Note({'velocity': [0, -10], 'radius': WHEEL_RADIUS/3, 'color': 'orange', 'delay': random.randint(0, 3)})

    # create center target
    target = PlayerWheel()

    # sets game start time for note delays
    game_time = time.time()

    # game loop
    while True:

        # for if the user exits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # screen resetting in the loop
        SCREEN.fill('white')

        # starts the game when the start button is pressed
        if start_button.pressed:

            # continues the game if no notes are missed
            if not left_note.miss and not right_note.miss and not top_note.miss and not bottom_note.miss:
                pygame.display.set_caption("Playing")

                # displaying the score
                score = str(left_note.score + right_note.score + top_note.score + bottom_note.score)

                score_font = pygame.font.SysFont("arial", 40)
                score_display = score_font.render('Score: ' + score, True, 'white', 'black')
                score_rect = score_display.get_rect()
                score_rect.center = (LENGTH / 2, HEIGHT / 8)
                SCREEN.blit(score_display, score_rect)

                # display her target
                target.update()

                # displaying notes if their delay is reached
                # updates to check not for misses and moves
                # increases speed of note
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

            # shows game over screen when any one note is missed
            else:
                # displays game over in app caption
                pygame.display.set_caption("Gameover")

                # initializes game over text
                #displays game over text
                go_font = pygame.font.SysFont("arial", 200)
                game_over = go_font.render('GAMEOVER', True, 'white', 'black')
                game_over_display = game_over.get_rect()
                game_over_display.center = (LENGTH / 2, HEIGHT / 2)
                SCREEN.blit(game_over, game_over_display)

                SCREEN.blit(score_display, score_rect)

                # creates back button
                back_button = MenuButton({'pos': [LENGTH / 2, HEIGHT * 2/ 3], 'txt': 'BACK', 'color': 'RED'})
                back_button.update()
                back_button.is_clicked()

                # resets back to the main menu
                if back_button.pressed:

                    # calling main() helps reset game_time so note speeding up resets per game
                    main()

        #displays how to text
        elif howto_button.pressed:
            howto_welcome = 'Welcome!'
            howto_about = 'This game is a simple, reaction-based game based on circles.'
            howto_goal = 'The goal is to make approaching notes disappear in the central target.'
            howto_controls = 'To make notes disappear, use the WASD or arrow keys to the corresponding side the note comes from!'
            howto_ex = 'For example, if a note is coming from the left of the target,press the "A" or LEFT arrow key to successfullly make it disappear.'
            howto_score = 'Making notes disappear closer to the center of the target will award more points to your score.'
            howto_gameover = 'Make sure to not over or under estimate the note! If the note disappears before or after the target it will be a game over.'
            howto_speed = 'The longer you play a single game, the faster the notes will move.'
            howto_prompt = 'Try it out!'

            howto_font = pygame.font.SysFont("arial", 35)

            # quick function for showing all the howto text
            def show_text(text, h):
                howto_display = howto_font.render(text, True, 'black', 'white')
                howto_rect = howto_display.get_rect()
                howto_rect.center = (LENGTH / 2, h)
                SCREEN.blit(howto_display, howto_rect)

            # shows howto text
            show_text(howto_welcome, 100)
            show_text(howto_about, 200)
            show_text(howto_goal, 300)
            show_text(howto_controls, 400)
            show_text(howto_ex, 500)
            show_text(howto_score, 600)
            show_text(howto_gameover, 700)
            show_text(howto_speed, 800)
            show_text(howto_prompt, 900)

            # creates and shows the back button
            back_button = MenuButton({'pos': [LENGTH / 2, 1000], 'txt': 'BACK', 'color': 'black'})
            back_button.update()
            back_button.is_clicked()

            # reset back to main menu
            if back_button.pressed:
                main()

        # selecting difficulty menu
        elif seldiff_button.pressed:
            # display selecting difficulty in app caption
            pygame.display.set_caption("Selecting Difficulty")

            # displaying th different difficulty buttons
            easy_button = MenuButton({'pos': [LENGTH / 2, 400], 'txt': 'EASY', 'color': 'green'})
            med_button = MenuButton({'pos': [LENGTH / 2, 600], 'txt': 'MEDIUM', 'color': 'orange'})
            hard_button = MenuButton({'pos': [LENGTH /2, 800], 'txt': 'HARD', 'color': 'red'})

            # select difficulty for each button
            # reassign a global variables so that difficulty will carry over even when the game is reset after game over
            easy_button.update()
            easy_button.is_clicked()
            if easy_button.pressed:
                difficulty = 0
                diff = 'EASY'

            med_button.update()
            med_button.is_clicked()
            if med_button.pressed:
                difficulty = 1
                diff = 'MEDIUM'

            hard_button.update()
            hard_button.is_clicked()
            if hard_button.pressed:
                difficulty = 2
                diff = 'HARD'

            # creates and shows back button
            back_button = MenuButton({'pos': [LENGTH / 2, HEIGHT / 8], 'txt': 'BACK', 'color': 'black'})
            back_button.update()
            back_button.is_clicked()

            # text for current difficulty selection caption
            font = pygame.font.SysFont("arial", 35)

            diff_display = font.render('Your current difficulty is ' + diff + '. ' + str(difficulty + 2) + ' notes will appear on screen at a time.', True, 'black', 'white')
            diff_rect = diff_display.get_rect()
            diff_rect.center = (LENGTH / 2, 1000)
            SCREEN.blit(diff_display, diff_rect)

            about_display = font.render('Increasing difficulty will increase the number of notes at a time.', True, 'black', 'white')
            about_rect = about_display.get_rect()
            about_rect.center = (LENGTH / 2, 1200)
            SCREEN.blit(about_display, about_rect)

            # reset menu to main menu
            if back_button.pressed:
                main()

        # display main menu when no buttons are in the 'is clicked' state
        else:
            pygame.display.set_caption("Main Menu")

            # displays and checks the clicked state of each button
            start_button.update()
            start_button.is_clicked()

            howto_button.update()
            howto_button.is_clicked()

            seldiff_button.update()
            seldiff_button.is_clicked()

        # updates pygame display
        pygame.display.update()

        # ticks a frame for the game loop
        FramePerSecond.tick(FPS)


#calls main function to run game
if __name__ == '__main__':
    main()
