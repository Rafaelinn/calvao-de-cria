import pygame
from sprites import *
from config import *
import sys
from pygame import mixer

pygame.display.set_caption("Calvão de Cria 1.0")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('arial.ttf', 32)

        self.character_spritesheet = Spritesheet('images/character.png')
        self.terrain_spritesheet = Spritesheet('images/terrain.png')
        self.carpet_spritesheet = Spritesheet('images/carpet.png')
        self.enemytile_spritesheet = Spritesheet('images/enemytile.png')
        self.enemy_spritesheet = Spritesheet('images/enemy.png')
        self.attack_spritesheet = Spritesheet('images/attack.png')
        self.intro_background = pygame.image.load('./images/introbackground.png')
        self.go_background = pygame.image.load('./images/gameover.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground1(self, j, i)
                if column == "C":
                    Ground2(self, j, i)
                if column == "B":
                    Block1(self, j, i)
                if column == "T":
                    Block2(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                    Ground3(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                    Ground2(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.counter = pygame.sprite.LayeredUpdates()

        self.createTilemap()
        pygame.mixer.Channel(0).set_volume(0.2)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('soundtrack/music.mp3'))
        self.score = 0
        self.hp = 100

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Channel(1).set_volume(0.1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('soundtrack/sword.mp3'))
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_h:
                    pygame.mixer.Channel(4).set_volume(0.3)
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('soundtrack/clash.mp3'))

                if event.key == pygame.K_1:
                    pygame.mixer.Channel(5).set_volume(0.1)
                    pygame.mixer.Channel(5).play(pygame.mixer.Sound('soundtrack/rat .mp3'))

                if event.key == pygame.K_k:
                    for i, row in enumerate(tilemap):
                        for j, column in enumerate(row):
                            if column == "E":
                                Enemy(self, j, i)

                if event.key == pygame.K_r:
                    self.new()
                    self.main()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        self.msg1 = f'Score: {self.score}'
        self.text1 = self.font.render(self.msg1,False,WHITE)
        self.screen.blit(self.text1,(80, 20))
        self.msg2 = f'HP: {self.hp}'
        self.text2 = self.font.render(self.msg2,False,WHITE)
        self.screen.blit(self.text2,(1050, 20))
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        restart_button = Button(700, WIN_HEIGHT - 300, 180, 70, WHITE, BLACK, 'Recomeçar', 32)
        exit_button = Button(700, WIN_HEIGHT - 200, 180, 70, WHITE, BLACK, 'Sair', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.new()
                self.main()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        play_button = Button(790, 410, 100, 50, WHITE, BLACK, 'Jogar', 32)
        exit_button = Button(790, 500, 100, 50, WHITE, BLACK, 'Sair', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_RETURN]:
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
