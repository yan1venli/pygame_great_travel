from settings import *
import pygame
import math
from map import collision_walls
from drawing import Drawing


class Player:
    def __init__(self, sprites, sc, x, y, heart, eat, energy, money, inventory):

        self.x, self.y = x, y
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004
        self.speed = player_speed
        self.screen = sc
        # collision parameters
        self.side = 50
        self.rect = pygame.Rect(*(HALF_WIDTH // 4, HALF_HEIGHT - 50), self.side, self.side)
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites
        self.fontObj = pygame.font.Font('C:\\Windows\\Fonts\\arial.ttf', 20)

        self.inventory = inventory
        self.name_item = []
        self.massa = 0
        self.max_massa = 30

        self.in_hand = "hand"
        self.create_player()
        self.heart = heart
        self.eat = eat
        self.energy = energy
        self.money = money

    # управление
    @property
    def pos(self):
        return (self.x, self.y)

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sound = pygame.mixer.Sound('sound\\effects\\run.ogg')
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.detect_collision(dx, dy)
            sound.stop()
            sound.play()
        if keys[pygame.K_s]:
            dx = -self.speed * cos_a
            dy = -self.speed * sin_a
            self.detect_collision(dx, dy)
            sound.stop()
            sound.play()
        if keys[pygame.K_a]:
            dx = self.speed * sin_a
            dy = -self.speed * cos_a
            self.detect_collision(dx, dy)
            sound.stop()
            sound.play()
        if keys[pygame.K_d]:
            dx = -self.speed * sin_a
            dy = self.speed * cos_a
            self.detect_collision(dx, dy)
            sound.stop()
            sound.play()
        if keys[pygame.K_e]:
            self.connect()

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def connect(self):
        if 133 < self.x < 250 and 133 < self.y < 250:
            self.speed = 5
            self.horse_base_sprite = pygame.image.load('sprites/horse/base/0.png').convert_alpha()
            self.horse_rect = self.horse_base_sprite.get_rect()
            self.horse_pos = (200, 200)
            self.screen.blit(self.horse_base_sprite, self.horse_pos)

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

    # инвентарь
    def inventorys(self):
        return self.inventory

    def add(self, item, massa, name):
        if self.massa + massa < self.max_massa:
            self.inventory.append(item)
            self.name_item.append(name)
            return f"Вы подобрали {item}"
        return "Нет места"

    def hand(self):
        if self.in_hand != "hand":
            name = self.name_item[self.inventory.index(self.in_hand)]
            return name

    def create_player(self):
        self.fontObj = pygame.font.Font('fonts\\arial.ttf', 20)
        v = [self.fontObj.render(f"телосложение", True, WHITE), self.fontObj.render(f"бег", True, WHITE),
             self.fontObj.render(f"сила", True, WHITE), self.fontObj.render(f"физическая вын.", True, WHITE),
             self.fontObj.render(f"моральная вын.", True, WHITE),
             self.fontObj.render(f"акробатика", True, WHITE),
             self.fontObj.render(f"фектование", True, WHITE), self.fontObj.render(f"скрытность", True, WHITE),
             self.fontObj.render(f"воровство", True, WHITE), self.fontObj.render(f"история", True, WHITE),
             self.fontObj.render(f"религия", True, WHITE), self.fontObj.render(f"наука", True, WHITE),
             self.fontObj.render(f"философия", True, WHITE), self.fontObj.render(f"логика", True, WHITE),
             self.fontObj.render(f"наблюдательность", True, WHITE),
             self.fontObj.render(f"монолог", True, WHITE),
             self.fontObj.render(f"диалог", True, WHITE)]

        pygame.mixer.music.load('sound\\music\\Mystic RPG — Epic Fantasy Inn Music.mp3')
        pygame.mixer.music.play()
        sound = pygame.mixer.Sound('sound\\effects\\button.ogg')
        poi_nts = v[0].get_rect()
        poi_nts.center = (350, 75)
        self.screen.blit(v[0], poi_nts)
        poi_nts = v[1].get_rect()
        poi_nts.center = (350, 125)
        self.screen.blit(v[1], poi_nts)
        poi_nts = v[2].get_rect()
        poi_nts.center = (350, 175)
        self.screen.blit(v[2], poi_nts)
        poi_nts = v[3].get_rect()
        poi_nts.center = (350, 235)
        self.screen.blit(v[3], poi_nts)
        poi_nts = v[4].get_rect()
        poi_nts.center = (350, 285)
        self.screen.blit(v[4], poi_nts)
        poi_nts = v[5].get_rect()
        poi_nts.center = (350, 345)
        self.screen.blit(v[5], poi_nts)
        poi_nts = v[6].get_rect()
        poi_nts.center = (350, 395)
        self.screen.blit(v[6], poi_nts)
        poi_nts = v[7].get_rect()
        poi_nts.center = (350, 445)
        self.screen.blit(v[7], poi_nts)
        poi_nts = v[8].get_rect()
        poi_nts.center = (350, 495)
        self.screen.blit(v[8], poi_nts)
        poi_nts = v[9].get_rect()
        poi_nts.center = (350, 555)
        self.screen.blit(v[9], poi_nts)
        poi_nts = v[10].get_rect()
        poi_nts.center = (350, 605)
        self.screen.blit(v[10], poi_nts)
        poi_nts = v[11].get_rect()
        poi_nts.center = (350, 655)
        self.screen.blit(v[11], poi_nts)
        poi_nts = v[12].get_rect()
        poi_nts.center = (350, 705)
        self.screen.blit(v[12], poi_nts)
        poi_nts = v[13].get_rect()
        poi_nts.center = (350, 755)
        self.screen.blit(v[13], poi_nts)
        poi_nts = v[14].get_rect()
        poi_nts.center = (330, 805)
        self.screen.blit(v[14], poi_nts)
        poi_nts = v[15].get_rect()
        poi_nts.center = (350, 865)
        self.screen.blit(v[15], poi_nts)
        poi_nts = v[16].get_rect()
        poi_nts.center = (350, 915)
        self.screen.blit(v[16], poi_nts)

        d = self.fontObj.render(f"5", True, WHITE)
        for i in range(3):
            poi_nts = d.get_rect()
            poi_nts.center = (450, 75 + 50 * i)
            self.screen.blit(d, poi_nts)
        for i in range(2):
            poi_nts = d.get_rect()
            poi_nts.center = (450, 235 + 50 * i)
            self.screen.blit(d, poi_nts)
        for i in range(4):
            poi_nts = d.get_rect()
            poi_nts.center = (450, 345 + 50 * i)
            self.screen.blit(d, poi_nts)
        for i in range(6):
            poi_nts = d.get_rect()
            poi_nts.center = (450, 555 + 50 * i)
            self.screen.blit(d, poi_nts)
        for i in range(2):
            poi_nts = d.get_rect()
            poi_nts.center = (450, 865 + 50 * i)
            self.screen.blit(d, poi_nts)

        pygame.draw.rect(self.screen, WHITE, (200, 50, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 100, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 150, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 210, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 260, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 320, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 370, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 420, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 470, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 530, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 580, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 630, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 680, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 730, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 780, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 840, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (200, 890, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (WIDTH - 300, 0, 300, HALF_HEIGHT + 200), 3)

        pygame.draw.polygon(self.screen, WHITE, ((510, 50), (560, 75), (510, 100)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 100), (560, 125), (510, 150)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 150), (560, 175), (510, 200)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 210), (560, 235), (510, 260)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 260), (560, 285), (510, 310)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 320), (560, 345), (510, 370)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 370), (560, 395), (510, 420)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 420), (560, 445), (510, 470)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 470), (560, 495), (510, 520)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 530), (560, 555), (510, 580)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 580), (560, 605), (510, 630)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 630), (560, 655), (510, 680)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 680), (560, 705), (510, 730)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 730), (560, 755), (510, 780)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 780), (560, 805), (510, 830)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 840), (560, 865), (510, 890)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((510, 890), (560, 915), (510, 940)), 3)

        pygame.draw.polygon(self.screen, WHITE, ((190, 50), (140, 75), (190, 100)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 100), (140, 125), (190, 150)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 150), (140, 175), (190, 200)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 210), (140, 235), (190, 260)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 260), (140, 285), (190, 310)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 320), (140, 345), (190, 370)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 370), (140, 395), (190, 420)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 420), (140, 445), (190, 470)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 470), (140, 495), (190, 520)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 530), (140, 555), (190, 580)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 580), (140, 605), (190, 630)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 630), (140, 655), (190, 680)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 680), (140, 705), (190, 730)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 730), (140, 755), (190, 780)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 780), (140, 805), (190, 830)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 840), (140, 865), (190, 890)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((190, 890), (140, 915), (190, 940)), 3)

        pygame.draw.line(self.screen, WHITE, (160, 75), (180, 75))
        pygame.draw.line(self.screen, WHITE, (160, 125), (180, 125))
        pygame.draw.line(self.screen, WHITE, (160, 175), (180, 175))
        pygame.draw.line(self.screen, WHITE, (160, 235), (180, 235))
        pygame.draw.line(self.screen, WHITE, (160, 285), (180, 285))
        pygame.draw.line(self.screen, WHITE, (160, 345), (180, 345))
        pygame.draw.line(self.screen, WHITE, (160, 395), (180, 395))
        pygame.draw.line(self.screen, WHITE, (160, 445), (180, 445))
        pygame.draw.line(self.screen, WHITE, (160, 495), (180, 495))
        pygame.draw.line(self.screen, WHITE, (160, 555), (180, 555))
        pygame.draw.line(self.screen, WHITE, (160, 605), (180, 605))
        pygame.draw.line(self.screen, WHITE, (160, 655), (180, 655))
        pygame.draw.line(self.screen, WHITE, (160, 705), (180, 705))
        pygame.draw.line(self.screen, WHITE, (160, 755), (180, 755))
        pygame.draw.line(self.screen, WHITE, (160, 805), (180, 805))
        pygame.draw.line(self.screen, WHITE, (160, 865), (180, 865))
        pygame.draw.line(self.screen, WHITE, (160, 915), (180, 915))

        pygame.draw.line(self.screen, WHITE, (520, 75), (540, 75))
        pygame.draw.line(self.screen, WHITE, (520, 125), (540, 125))
        pygame.draw.line(self.screen, WHITE, (520, 175), (540, 175))
        pygame.draw.line(self.screen, WHITE, (520, 235), (540, 235))
        pygame.draw.line(self.screen, WHITE, (520, 285), (540, 285))
        pygame.draw.line(self.screen, WHITE, (520, 345), (540, 345))
        pygame.draw.line(self.screen, WHITE, (520, 395), (540, 395))
        pygame.draw.line(self.screen, WHITE, (520, 445), (540, 445))
        pygame.draw.line(self.screen, WHITE, (520, 495), (540, 495))
        pygame.draw.line(self.screen, WHITE, (520, 555), (540, 555))
        pygame.draw.line(self.screen, WHITE, (520, 605), (540, 605))
        pygame.draw.line(self.screen, WHITE, (520, 655), (540, 655))
        pygame.draw.line(self.screen, WHITE, (520, 705), (540, 705))
        pygame.draw.line(self.screen, WHITE, (520, 755), (540, 755))
        pygame.draw.line(self.screen, WHITE, (520, 805), (540, 805))
        pygame.draw.line(self.screen, WHITE, (520, 865), (540, 865))
        pygame.draw.line(self.screen, WHITE, (520, 915), (540, 915))

        pygame.draw.line(self.screen, WHITE, (530, 65), (530, 85))
        pygame.draw.line(self.screen, WHITE, (530, 115), (530, 135))
        pygame.draw.line(self.screen, WHITE, (530, 165), (530, 185))
        pygame.draw.line(self.screen, WHITE, (530, 225), (530, 245))
        pygame.draw.line(self.screen, WHITE, (530, 275), (530, 295))
        pygame.draw.line(self.screen, WHITE, (530, 335), (530, 355))
        pygame.draw.line(self.screen, WHITE, (530, 385), (530, 405))
        pygame.draw.line(self.screen, WHITE, (530, 435), (530, 455))
        pygame.draw.line(self.screen, WHITE, (530, 485), (530, 505))
        pygame.draw.line(self.screen, WHITE, (530, 545), (530, 565))
        pygame.draw.line(self.screen, WHITE, (530, 595), (530, 615))
        pygame.draw.line(self.screen, WHITE, (530, 645), (530, 665))
        pygame.draw.line(self.screen, WHITE, (530, 695), (530, 715))
        pygame.draw.line(self.screen, WHITE, (530, 745), (530, 765))
        pygame.draw.line(self.screen, WHITE, (530, 795), (530, 815))
        pygame.draw.line(self.screen, WHITE, (530, 855), (530, 875))
        pygame.draw.line(self.screen, WHITE, (530, 905), (530, 925))

        running = True
        points = 20
        physigue = run = forses = 5
        physical = moral = 5
        acrobatics = fencing = stels = treft = 5
        history = religion = science = philophy = logic = observation = 5
        monologue = dialogue = 5

        point = self.fontObj.render(f"Очки: {points}", True, WHITE)
        poi_nts = point.get_rect()
        poi_nts.center = (350, 30)
        self.screen.blit(point, poi_nts)

        pygame.draw.rect(self.screen, WHITE, (WIDTH - 300, HEIGHT - 100, 300, 50), 3)
        point = self.fontObj.render(f"Продолжить", True, WHITE)
        poi_nts = point.get_rect()
        poi_nts.center = (WIDTH - 150, HEIGHT - 75)
        self.screen.blit(point, poi_nts)

        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    exit()
                if 200 < mouse[0] < 500:
                    if 50 < mouse[1] < 100:
                        pass
                    elif 100 < mouse[1] < 150:
                        pass
                    elif 150 < mouse[1] < 200:
                        pass
                    elif 210 < mouse[1] < 260:
                        pass
                    elif 260 < mouse[1] < 310:
                        pass
                    elif 320 < mouse[1] < 370:
                        pass
                    elif 370 < mouse[1] < 420:
                        pass
                    elif 420 < mouse[1] < 470:
                        pass
                    elif 470 < mouse[1] < 520:
                        pass
                    elif 530 < mouse[1] < 580:
                        pass
                    elif 580 < mouse[1] < 630:
                        pass
                    elif 630 < mouse[1] < 680:
                        pass
                    elif 680 < mouse[1] < 730:
                        pass
                    elif 740 < mouse[1] < 790:
                        pass
                    elif 790 < mouse[1] < 840:
                        pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        sound.play()
                        if HEIGHT - 100 < mouse[1] < HEIGHT - 50 and WIDTH - 300 < mouse[0] < WIDTH:
                            running = False
                            break
                        if 140 < mouse[0] < 190:
                            if 50 < mouse[1] < 100 and physigue > 1:
                                physigue -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 55, 40, 40))
                                b1 = self.fontObj.render(f'{physigue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 75)
                                self.screen.blit(b1, t1)
                            elif 100 < mouse[1] < 150 and run > 1:
                                run -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 105, 40, 40))
                                b1 = self.fontObj.render(f'{run}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 125)
                                self.screen.blit(b1, t1)
                            elif 150 < mouse[1] < 200 and forses > 1:
                                forses -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 155, 40, 40))
                                b1 = self.fontObj.render(f'{forses}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 175)
                                self.screen.blit(b1, t1)
                            elif 210 < mouse[1] < 260 and physical > 1:
                                physical -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 215, 40, 40))
                                b1 = self.fontObj.render(f'{physical}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 235)
                                self.screen.blit(b1, t1)
                            elif 260 < mouse[1] < 310 and moral > 1:
                                moral -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 265, 40, 40))
                                b1 = self.fontObj.render(f'{moral}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 285)
                                self.screen.blit(b1, t1)
                            elif 320 < mouse[1] < 370 and acrobatics > 1:
                                acrobatics -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 325, 40, 40))
                                b1 = self.fontObj.render(f'{acrobatics}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 345)
                                self.screen.blit(b1, t1)
                            elif 370 < mouse[1] < 420 and fencing > 1:
                                fencing -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 375, 40, 40))
                                b1 = self.fontObj.render(f'{fencing}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 395)
                                self.screen.blit(b1, t1)
                            elif 420 < mouse[1] < 470 and stels > 1:
                                stels -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 425, 40, 40))
                                b1 = self.fontObj.render(f'{stels}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 445)
                                self.screen.blit(b1, t1)
                            elif 470 < mouse[1] < 520 and treft > 1:
                                treft -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 475, 40, 40))
                                b1 = self.fontObj.render(f'{treft}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 495)
                                self.screen.blit(b1, t1)
                            elif 530 < mouse[1] < 580 and history > 1:
                                history -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 535, 40, 40))
                                b1 = self.fontObj.render(f'{history}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 555)
                                self.screen.blit(b1, t1)
                            elif 580 < mouse[1] < 630 and religion > 1:
                                religion -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 585, 40, 40))
                                b1 = self.fontObj.render(f'{religion}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 605)
                                self.screen.blit(b1, t1)
                            elif 630 < mouse[1] < 680 and science > 1:
                                science -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 635, 40, 40))
                                b1 = self.fontObj.render(f'{science}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 655)
                                self.screen.blit(b1, t1)
                            elif 680 < mouse[1] < 730 and philophy > 1:
                                philophy -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 685, 40, 40))
                                b1 = self.fontObj.render(f'{philophy}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 705)
                                self.screen.blit(b1, t1)
                            elif 730 < mouse[1] < 780 and logic > 1:
                                logic -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 735, 40, 40))
                                b1 = self.fontObj.render(f'{logic}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 755)
                                self.screen.blit(b1, t1)
                            elif 780 < mouse[1] < 830 and observation > 1:
                                observation -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 785, 40, 40))
                                b1 = self.fontObj.render(f'{observation}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 805)
                                self.screen.blit(b1, t1)
                            elif 840 < mouse[1] < 890 and dialogue > 1:
                                dialogue -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 845, 40, 40))
                                b1 = self.fontObj.render(f'{dialogue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 865)
                                self.screen.blit(b1, t1)
                            elif 890 < mouse[1] < 940 and monologue > 1:
                                monologue -= 1
                                points += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 895, 40, 40))
                                b1 = self.fontObj.render(f'{monologue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 915)
                                self.screen.blit(b1, t1)
                        if 510 < mouse[0] < 560 and points > 0:
                            if 50 < mouse[1] < 100 and physigue < 15:
                                physigue += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 55, 40, 40))
                                b1 = self.fontObj.render(f'{physigue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 75)
                                self.screen.blit(b1, t1)
                            elif 100 < mouse[1] < 150 and run < 15:
                                run += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 105, 40, 40))
                                b1 = self.fontObj.render(f'{run}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 125)
                                self.screen.blit(b1, t1)
                            elif 150 < mouse[1] < 200 and forses < 15:
                                forses += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 155, 40, 40))
                                b1 = self.fontObj.render(f'{forses}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 175)
                                self.screen.blit(b1, t1)
                            elif 210 < mouse[1] < 260 and physical < 15:
                                physical += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 215, 40, 40))
                                b1 = self.fontObj.render(f'{physical}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 235)
                                self.screen.blit(b1, t1)
                            elif 260 < mouse[1] < 310 and moral < 15:
                                moral += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 265, 40, 40))
                                b1 = self.fontObj.render(f'{moral}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 285)
                                self.screen.blit(b1, t1)
                            elif 320 < mouse[1] < 370 and acrobatics < 15:
                                acrobatics += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 325, 40, 40))
                                b1 = self.fontObj.render(f'{acrobatics}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 345)
                                self.screen.blit(b1, t1)
                            elif 370 < mouse[1] < 420 and fencing < 15:
                                fencing += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 375, 40, 40))
                                b1 = self.fontObj.render(f'{fencing}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 395)
                                self.screen.blit(b1, t1)
                            elif 420 < mouse[1] < 470 and stels < 15:
                                stels += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 425, 40, 40))
                                b1 = self.fontObj.render(f'{stels}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 445)
                                self.screen.blit(b1, t1)
                            elif 470 < mouse[1] < 520 and treft < 15:
                                treft += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 475, 40, 40))
                                b1 = self.fontObj.render(f'{treft}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 495)
                                self.screen.blit(b1, t1)
                            elif 530 < mouse[1] < 580 and history < 15:
                                history += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 535, 40, 40))
                                b1 = self.fontObj.render(f'{history}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 555)
                                self.screen.blit(b1, t1)
                            elif 580 < mouse[1] < 630 and religion < 15:
                                religion += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 585, 40, 40))
                                b1 = self.fontObj.render(f'{religion}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 605)
                                self.screen.blit(b1, t1)
                            elif 630 < mouse[1] < 680 and science < 15:
                                science += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 635, 40, 40))
                                b1 = self.fontObj.render(f'{science}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 655)
                                self.screen.blit(b1, t1)
                            elif 680 < mouse[1] < 730 and philophy < 15:
                                philophy += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 685, 40, 40))
                                b1 = self.fontObj.render(f'{philophy}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 705)
                                self.screen.blit(b1, t1)
                            elif 730 < mouse[1] < 780 and logic < 15:
                                logic += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 735, 40, 40))
                                b1 = self.fontObj.render(f'{logic}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 755)
                                self.screen.blit(b1, t1)
                            elif 780 < mouse[1] < 830 and observation < 15:
                                observation += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 785, 40, 40))
                                b1 = self.fontObj.render(f'{observation}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 805)
                                self.screen.blit(b1, t1)
                            elif 840 < mouse[1] < 890 and dialogue < 15:
                                dialogue += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 845, 40, 40))
                                b1 = self.fontObj.render(f'{dialogue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 865)
                                self.screen.blit(b1, t1)
                            elif 890 < mouse[1] < 940 and monologue < 15:
                                monologue += 1
                                points -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (430, 895, 40, 40))
                                b1 = self.fontObj.render(f'{monologue}', True, WHITE)
                                t1 = b1.get_rect()
                                t1.center = (450, 915)
                                self.screen.blit(b1, t1)
                pygame.draw.rect(self.screen, (0, 0, 0), (310, 5, 80, 40))
                point = self.fontObj.render(f"Очки: {points}", True, WHITE)
                poi_nts = point.get_rect()
                poi_nts.center = (350, 30)
                self.screen.blit(point, poi_nts)

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH - 300, HEIGHT + 400))

        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 150, 100, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 150, 300, 300, 50), 3)
        pygame.draw.rect(self.screen, WHITE, (HALF_WIDTH - 150, 500, 300, 50), 3)

        pygame.draw.polygon(self.screen, WHITE, ((HALF_WIDTH + 160, 100), (HALF_WIDTH + 210, 125), (HALF_WIDTH + 160, 150)), 3)
        pygame.draw.polygon(self.screen, WHITE, ((HALF_WIDTH + 160, 300), (HALF_WIDTH + 210, 325), (HALF_WIDTH + 160, 350)), 3)

        pygame.draw.polygon(self.screen, WHITE,
                            ((HALF_WIDTH - 160, 100), (HALF_WIDTH - 210, 125), (HALF_WIDTH - 160, 150)), 3)
        pygame.draw.polygon(self.screen, WHITE,
                            ((HALF_WIDTH - 160, 300), (HALF_WIDTH - 210, 325), (HALF_WIDTH - 160, 350)), 3)

        nacional_name = [self.fontObj.render(f"Лютанин", True, WHITE), self.fontObj.render(f"Бостард", True, WHITE),
                         self.fontObj.render(f"Иман", True, WHITE), self.fontObj.render(f"Рокалин", True, WHITE),
                         self.fontObj.render(f"Джеразиан", True, WHITE),
                         self.fontObj.render(f"Ламанагрин", True, WHITE),
                         self.fontObj.render(f"Алададин", True, WHITE), self.fontObj.render(f"Браусилин", True, WHITE)
                         ]
        nacional = []
        road_name = [self.fontObj.render(f"наёмник", True, WHITE),
                     self.fontObj.render(f"странник", True, WHITE),
                     self.fontObj.render(f"школяр", True, WHITE),
                     self.fontObj.render(f"торговец", True, WHITE)]
        road = []
        i = 0
        j = 0
        b1 = road_name[i]
        t1 = b1.get_rect()
        t1.center = (HALF_WIDTH, 125)
        self.screen.blit(b1, t1)
        b1 = nacional_name[j]
        t1 = b1.get_rect()
        t1.center = (HALF_WIDTH, 325)
        self.screen.blit(b1, t1)
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        sound.play()
                        if HEIGHT - 100 < mouse[1] < HEIGHT - 50 and WIDTH - 300 < mouse[0] < WIDTH:
                            running = False
                            break
                        if HALF_WIDTH - 210 < mouse[0] < HALF_WIDTH - 160:
                            if 100 < mouse[1] < 150:
                                if i == 0:
                                    i = 3
                                else:
                                    i -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (HALF_WIDTH - 50, 105, 100, 40))
                                b1 = road_name[i]
                                t1 = b1.get_rect()
                                t1.center = (HALF_WIDTH, 125)
                                self.screen.blit(b1, t1)
                            if 300 < mouse[1] < 350:
                                if j == 0:
                                    j = 7
                                else:
                                    j -= 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (HALF_WIDTH - 60, 305, 120, 40))
                                b1 = nacional_name[j]
                                t1 = b1.get_rect()
                                t1.center = (HALF_WIDTH, 325)
                                self.screen.blit(b1, t1)
                        if HALF_WIDTH + 160 < mouse[0] < HALF_WIDTH + 210:
                            if 100 < mouse[1] < 150:
                                if i == 3:
                                    i = 0
                                else:
                                    i += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (HALF_WIDTH - 50, 105, 100, 40))
                                b1 = road_name[i]
                                t1 = b1.get_rect()
                                t1.center = (HALF_WIDTH, 125)
                                self.screen.blit(b1, t1)
                            if 300 < mouse[1] < 350:
                                if j == 7:
                                    j = 0
                                else:
                                    j += 1
                                pygame.draw.rect(self.screen, (0, 0, 0), (HALF_WIDTH - 60, 305, 160, 40))
                                b1 = nacional_name[j]
                                t1 = b1.get_rect()
                                t1.center = (HALF_WIDTH, 325)
                                self.screen.blit(b1, t1)

    def draw_hp(self):
        pygame.draw.line(self.screen, RED, (20, HEIGHT - 10 - (self.heart * 1.5)), (20, HEIGHT - 10), 4)
        pygame.draw.line(self.screen, BLUE, (30, HEIGHT - 10 - (self.energy * 1.5)), (30, HEIGHT - 10), 4)
        pygame.draw.line(self.screen, YELLOW, (40, HEIGHT - 10 - (self.eat * 1.5)), (40, HEIGHT - 10), 4)

    def returns(self):
        return self.x, self.y, self.heart, self.energy, self.eat, self.money, self.inventory
