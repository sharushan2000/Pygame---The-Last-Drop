import pygame
import random
import math
from pygame import mixer


class LastDrop:
    # initialize pygame
    pygame.init()

    def __init__(self):

        self.IS_PLAYING = True  # main loop
        self.QUIT = False

        self.SCORE = 0  # points
        self.SCORE_FONT = pygame.font.Font('freesansbold.ttf', 25)
        self.SCORE_X = 0  # score text x coordinate
        self.SCORE_y = 0  # score text y coordinates
        self.SCORE_COLOUR = (0, 222, 255)

        self.TEXT_FONT = pygame.font.Font('freesansbold.ttf', 20)
        self.TEXT_COLOUR = (52, 192, 213)
        self.LAST_SCORE = 0

        self.W_WIDTH, self.W_HEIGHT = 400, 600  # game window width ,height
        self.WINDOW = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))  # game window / surface

        self.ICON = pygame.transform.scale(pygame.image.load('icon.png'), (100, 100))  # game icon
        pygame.display.set_caption("The Last Drop ")  # adding caption to game window
        pygame.display.set_icon(self.ICON)  # addig icon

        self.VEL = 3  # player starting phase velocity

        self.LEVEL_UP_FLAG = False  # flag to increase speed

        # self.RED = (10, 10, 10)

        self.FPS = 60  # Frames Per Second
        self.BG_COLOR = (76, 176, 223)  # Background colour
        self.BG_IMG = pygame.image.load("dark-background.jpg")
        self.BG_SKY = pygame.transform.scale(self.BG_IMG, (self.W_WIDTH, self.W_HEIGHT))

        self.PLAYER_DROP_IMAGE = pygame.image.load('drop.png')
        self.PLAYER_WIDTH, self.PLAYER_HEIGHT = 30, 30
        # Scaling and Rotating the PLAYER_DROP_IMAGE
        self.PLAYER_DROP = pygame.transform.rotate(
            pygame.transform.scale(self.PLAYER_DROP_IMAGE, (self.PLAYER_WIDTH, self.PLAYER_HEIGHT)), 180)

        mixer.music.load('bg.mp3')  # Background Music
        mixer.music.play(-1)  # loop

        self.DROP_CONFLICT_SOUND = mixer.Sound('conflict.mp3')  # Drops Conflict Sound

        # self.PLAYER_X, self.PLAYER_Y = 185, 450
        self.ENEMY_IMG = pygame.transform.scale(pygame.image.load('drop.png'), (30, 30))  # Enemy drop image
        self.ENEMY_LIST = []
        self.ENEMY_X = []
        self.ENEMY_Y = []
        self.ENEMY_VEl = 5
        self.NO_ENEMIES = 8

    def create_enemies(self):
        # adding enemy related elements to list
        for enemy in range(self.NO_ENEMIES):
            self.ENEMY_LIST.append(self.ENEMY_IMG)
            self.ENEMY_X.append(random.randint(5, 395))
            self.ENEMY_Y.append(random.randint(0, 70))

    def is_collision(self, player_x, player_y, enemy_x, enemy_y):
        # check for collision between drop
        distance = math.sqrt(
            math.pow((player_x + 15) - (enemy_x + 15), 2) + math.pow((player_y + 15) - (enemy_y + 15), 2))
        if distance < 19:
            self.DROP_CONFLICT_SOUND.play()  # play conflict souund
            self.IS_PLAYING = False
            self.LAST_SCORE = math.floor(self.add_score())  # capturing the last score

    def add_score(self):
        # calculating the player points
        if self.IS_PLAYING:
            self.SCORE += 0.01
            return math.floor(self.SCORE)
        else:
            return self.SCORE

    def show_score(self):
        # display player points
        score = self.SCORE_FONT.render("Score : " + str(self.add_score()), True, self.SCORE_COLOUR)
        self.WINDOW.blit(score, (self.SCORE_X, self.SCORE_y))

    def after_col(self):
        self.WINDOW.fill(self.BG_COLOR)
        self.WINDOW.blit(self.BG_SKY, (0, 0))
        # after game end
        text = self.TEXT_FONT.render(
            " Your Score : " + str(self.LAST_SCORE), True, self.TEXT_COLOUR)
        restart = self.TEXT_FONT.render("Restart Game : HIT - SPACEBAR - ", True, self.TEXT_COLOUR)
        quit = self.TEXT_FONT.render("Quit Game : HIT - Esc - ", True, self.TEXT_COLOUR)

        self.WINDOW.blit(text, (50, 300))
        self.WINDOW.blit(restart, (50, 350))
        self.WINDOW.blit(quit, (50, 400))

    def game_restart(self):
        # re-configuring
        self.IS_PLAYING = True
        self.VEL = 3
        self.ENEMY_VEl = 5
        self.SCORE = 0

    def level_up(self):
        # increasing the speed
        if self.LEVEL_UP_FLAG:  # checking for the flag
            if self.add_score() % 30 == 0:
                self.ENEMY_VEl += 0.02

            if self.add_score() % 50 == 0:
                self.VEL += 0.02

        else:
            if self.add_score() > 10:
                self.LEVEL_UP_FLAG = True

    def enemy_movement(self):
        # enemy drops movement
        for i in range(self.NO_ENEMIES):
            enemey = pygame.Rect(self.ENEMY_X[i], self.ENEMY_Y[i], 30, 30)
            # pygame.draw.rect(self.WINDOW, (255, 0, 0), enemey)

            self.WINDOW.blit(self.ENEMY_LIST[i], (enemey.x, enemey.y))
            if self.ENEMY_Y[i] >= 600:
                self.ENEMY_Y[i] = random.randint(0, 70)
                self.ENEMY_X[i] = random.randint(5, 395)

            else:
                self.is_collision(self.PLAYER.x, self.PLAYER.y, self.ENEMY_X[i], self.ENEMY_Y[i])

                self.ENEMY_Y[i] += self.ENEMY_VEl

    def window_draw(self, player):
        # all drawing
        self.WINDOW.fill(self.BG_COLOR)
        self.WINDOW.blit(self.BG_SKY, (0, 0))

        # pygame.draw.rect(self.WINDOW, (255, 255, 0), player)

        self.WINDOW.blit(self.PLAYER_DROP, (player.x, player.y))
        self.enemy_movement()
        self.show_score()

        pygame.display.update()

    def handle_player_movement(self, key_pressed, player):
        # handling the player movement
        if key_pressed[pygame.K_UP]:
            if player.y <= 0:
                player.y = 0
            else:
                player.y -= self.VEL

        if key_pressed[pygame.K_DOWN]:
            if player.y >= 575:
                player.y = 575
            else:
                player.y += self.VEL

        if key_pressed[pygame.K_LEFT]:
            if player.x <= 0:
                player.x = 0
            else:
                player.x -= self.VEL

        if key_pressed[pygame.K_RIGHT]:
            if player.x >= 375:
                player.x = 375
            else:
                player.x += self.VEL

    def main(self):
        # main function :
        self.create_enemies()
        clock = pygame.time.Clock()
        self.PLAYER = pygame.Rect(185, 450, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)
        while not self.QUIT:
            while self.IS_PLAYING:
                self.window_draw(self.PLAYER)
                self.level_up()
                clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.IS_PLAYING = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.IS_PLAYING = False

                key_pressed = pygame.key.get_pressed()
                self.handle_player_movement(key_pressed, self.PLAYER)

            self.ENEMY_LIST.clear()
            self.ENEMY_X.clear()
            self.ENEMY_Y.clear()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.QUIT = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.QUIT = True

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_SPACE]:
                self.create_enemies()
                self.game_restart()

            self.after_col()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    ls = LastDrop()
    ls.main()
