import pygame
import random
import math
from pygame import mixer


# initialize pygame
class LastDrop:
    pygame.init()

    def __init__(self):
        self.RUN = True

        self.W_WIDTH, self.W_HEIGHT = 400, 600
        self.WINDOW = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))

        pygame.display.set_caption("The Last Drop ")

        self.VEL = 3

        self.RED = (10, 10, 10)

        self.FPS = 60
        self.BG_COLOR = (255, 255, 255)

        PLAYER_DROP_IMAGE = pygame.image.load('drop.png')
        self.PLAYER_WIDTH, self.PLAYER_HEIGHT = 30, 30
        self.PLAYER_DROP = pygame.transform.rotate(
            pygame.transform.scale(PLAYER_DROP_IMAGE, (self.PLAYER_WIDTH, self.PLAYER_HEIGHT)), 180)

        BG_IMG = pygame.image.load('background-image.jpg')
        self.BG = pygame.transform.scale(BG_IMG, (400, 100))

        mixer.music.load('bg.mp3')
        mixer.music.play(-1)

        self.DROP_CONFLICT_SOUND = mixer.Sound('conflict.mp3')

        # self.PLAYER_X, self.PLAYER_Y = 185, 450
        self.ENEMY_IMG = pygame.transform.scale(pygame.image.load('drop.png'), (30, 30))
        self.ENEMY_LIST = []
        self.ENEMY_X = []
        self.ENEMY_Y = []
        self.ENEMY_VEl = 5
        self.NO_ENEMIES = 7

        for enemy in range(self.NO_ENEMIES):
            self.ENEMY_LIST.append(self.ENEMY_IMG)
            self.ENEMY_X.append(random.randint(5, 395))
            self.ENEMY_Y.append(random.randint(0, 70))

        print(self.ENEMY_LIST, self.ENEMY_X, self.ENEMY_Y)

    def is_collision(self, player_x, player_y, enemy_x, enemy_y):
        distance = math.sqrt(
            math.pow((player_x + 15) - (enemy_x + 15), 2) + math.pow((player_y + 15) - (enemy_y + 15), 2))
        if distance < 20:
            self.DROP_CONFLICT_SOUND.play()
            self.RUN = False

    def enemy_movement(self):
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
        self.WINDOW.fill(self.BG_COLOR)

        self.WINDOW.blit(self.BG, (0, 0))
        # pygame.draw.rect(self.WINDOW, (255, 255, 0), player)

        self.WINDOW.blit(self.PLAYER_DROP, (player.x, player.y))
        self.enemy_movement()

        pygame.display.update()

    def handle_player_movement(self, key_pressed, player):
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
        clock = pygame.time.Clock()
        self.PLAYER = pygame.Rect(185, 450, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)
        while self.RUN:
            clock.tick(self.FPS)
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.RUN = False

            key_pressed = pygame.key.get_pressed()
            self.handle_player_movement(key_pressed, self.PLAYER)

            self.window_draw(self.PLAYER)

        pygame.quit()


if __name__ == "__main__":
    ls = LastDrop()
    ls.main()
