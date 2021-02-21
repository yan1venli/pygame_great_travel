import pygame
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
sc_map = pygame.Surface(MINIMAP_RES)
sprites = Sprites()
clock = pygame.time.Clock()


def main(x=HALF_WIDTH // 4, y=HALF_HEIGHT - 50, heart=100, eat=100, energy=100, money=0, *inventory):
    player = Player(sprites, sc, x, y, heart, eat, energy, inventory, money)
    drawing = Drawing(sc, sc_map)
    pygame.mouse.set_visible(False)
    pygame.mixer.music.load('sound\\music\\Free Zen Spirit — Zen Spirit Music.mp3')
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        player.movement()
        sc.fill(BLACK)

        drawing.background(player.angle)
        walls = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        pygame.draw.rect(sc, BLACK, (WIDTH - 400, 0, 700, HEIGHT))
        pygame.draw.rect(sc, BLACK, (0, 0, WIDTH, 30))
        pygame.draw.rect(sc, BLACK, (0, HEIGHT - 50, WIDTH, 100))
        pygame.draw.rect(sc, WHITE, (WIDTH - 400, 0, 700, HEIGHT - 300), 3)
        pygame.draw.rect(sc, WHITE, (WIDTH - 400, HEIGHT - 300, 700, 300), 3)
        player.draw_hp()

        pygame.display.flip()
        clock.tick(FPS)
        '''
            if keys[pygame.K_SPACE]:
                if player_angle_z < 90:
                    player_angle_z += 1
                    COVERAGE = coverage(player_angle_z)
            if keys[pygame.K_b]:
                if player_angle_z > 0:
                    player_angle_z -= 1
                    COVERAGE = coverage(player_angle_z)
                '''


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.name = pygame.font.Font('fonts\\fantasy.ttf', 100)
        self.fontObj = pygame.font.Font('fonts\\fantasy.ttf', 50)
        self.menu()

    def menu(self):
        v = [
            self.name.render(f'Great Travel', True, WHITE),
            self.fontObj.render(f'Новая игра', True, WHITE), self.fontObj.render(f'Загрузить игру', True, WHITE),
            self.fontObj.render(f'Настройки', True, WHITE), self.fontObj.render(f'Выход', True, WHITE)]

        pygame.mixer.music.load('sound\\music\\Mystic RPG — Fantasy Music.mp3')
        pygame.mixer.music.play()
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 200, HALF_HEIGHT - 300, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 200, HALF_HEIGHT - 100, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 200, HALF_HEIGHT + 100, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 200, HALF_HEIGHT + 300, 400, 100), 3)
        poi_nts = v[0].get_rect()
        poi_nts.center = (HALF_WIDTH, 75)
        self.screen.blit(v[0], poi_nts)
        poi_nts = v[1].get_rect()
        poi_nts.center = (HALF_WIDTH, HALF_HEIGHT - 250)
        self.screen.blit(v[1], poi_nts)
        poi_nts = v[2].get_rect()
        poi_nts.center = (HALF_WIDTH, HALF_HEIGHT - 50)
        self.screen.blit(v[2], poi_nts)
        poi_nts = v[3].get_rect()
        poi_nts.center = (HALF_WIDTH, HALF_HEIGHT + 150)
        self.screen.blit(v[3], poi_nts)
        poi_nts = v[4].get_rect()
        poi_nts.center = (HALF_WIDTH, HALF_HEIGHT + 350)
        self.screen.blit(v[4], poi_nts)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pos()
                if keys[pygame.K_ESCAPE]:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if HALF_WIDTH - 200 < mouse[0] < HALF_WIDTH + 200:
                            if HALF_HEIGHT - 300 < mouse[1] < HALF_HEIGHT - 200:
                                running = False
                                break
                            elif HALF_HEIGHT - 100 < mouse[1] < HALF_HEIGHT:
                                self.load()
                            elif HALF_HEIGHT + 100 < mouse[1] < HALF_HEIGHT + 200:
                                self.settings()
                            elif HALF_HEIGHT + 300 < mouse[1] < HALF_HEIGHT + 400:
                                exit()
            pygame.display.flip()

        self.screen.fill(BLACK)

    def settings(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (WIDTH - 500, 100, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (WIDTH - 500, 300, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 200, HEIGHT - 400, 400, 100), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH + 250, HEIGHT - 400, 400, 100), 3)
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    exit()
                if keys[pygame.K_ESCAPE]:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HALF_WIDTH - 200 < mouse[0] < HALF_WIDTH + 200:
                        if HALF_HEIGHT - 300 < mouse[1] < HALF_HEIGHT - 200:
                            pass

    def load(self):
        self.save(100, 100, 100, 100, 100, 100, "я")
        f = open("save.txt", 'r')
        r = f.read()
        r = r[0::-1]
        r = r.split()
        #print(r)
        #for i in range(6):
        #    r[i] = int(r[i])
        #main(r[0], r[1], r[2], r[3], r[4], r[5], r[5:])

    def save(self, x, y, heart, energy, eat, money, inventory):
        f = open("save.txt", 'w')
        f.write(f"{x, y, heart, energy, eat, money, inventory} \n")
        f.close()


m = Menu(sc)
main()
