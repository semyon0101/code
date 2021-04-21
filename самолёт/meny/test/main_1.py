from class_ import *
import pygame

pygame.init()
pygame.display.set_caption("самолёт")

clock = pygame.time.Clock()

m_1 = 0

class Level:
    def __init__(self, _blocks: list, _enemies: list):
        self.blocks = _blocks
        self.enemies = _enemies
        self.m = 0
        self.max_hp = 100
        self.player = Player(self.max_hp)
        self.arial = pygame.font.SysFont("arial", 36)
        self.xp_model = {
            "Enemy_2": 20,
            "Enemy_1": 10,
        }
        self.lasers = []
        self.game_over = False
        self.win = False
        self.article = []
        self.end = False

    def handle_event(self, _event):
        for _some in self.article:
            _some.handle_event(_event)

    def update(self):
        if not debug and not self.game_over and not self.win:
            _over = self.player.update(self.blocks, self.enemies, self.lasers, self.blocks, self.enemies, self.m)
            if _over:
                self.player.hp -= 25
            for _laser in self.lasers:
                _over = _laser.update(self.player, self.lasers, self.enemies, self.xp_model, self.m)
                if _over:
                    self.player.hp -= 10
                if -abs(self.player.hp) == self.player.hp:
                    self.game_over = True

            if self.m >= 360 and not self.enemies:
                self.win = True

            for _enemy in self.enemies:
                _enemy.update(self.blocks, self.player, self.lasers, self.enemies, self.m)

        if not debug and not self.game_over and not self.win:
            self.m += 2

    def draw(self, _screen):
        for _block in self.blocks:
            _screen = _block.draw(_screen, self.m + m_1)

        for _laser in self.lasers:
            _screen = _laser.draw(self.lasers, _screen)

        for _enemy in self.enemies:
            _screen = _enemy.draw(_screen, self.m + m_1)

        _screen = self.player.draw(_screen, m_1)

        for _some in self.article:
            _screen = _some.draw(_screen)

        if self.game_over:
            self.end = True
            _surf = self.arial.render("game over", True, (255, 90, 65))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
        elif self.win:


            def func():
                pass

            _surf = self.arial.render("you win", True, (255, 90, 70))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
            if not self.end:
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 30, 120, 30], "in menu", func,
                                           border_x_y=[20,-1]))

            self.end = True

        if not debug:
            pygame.draw.rect(_screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
            pygame.draw.rect(_screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
            pygame.draw.rect(_screen,
                             [100 + (self.max_hp - max(self.player.hp, 0)) * (155 / self.max_hp),
                              255 - (self.max_hp - max(self.player.hp, 0)) * (155 / self.max_hp),
                              100], pygame.Rect([2, 2, 200 / self.max_hp * max(self.player.hp, 0), 50]))

            _surf = self.arial.render(str(max(self.player.hp, 0)) + " hp", True, (255, 255, 255))
            _screen.blit(_surf, [101.5 - _surf.get_rect()[2] / 2, 26.5 - _surf.get_rect()[3] / 2])

            _surf = self.arial.render(str(self.player.xp) + " xp", True, (255, 255, 255))
            _screen.blit(_surf, [450 - _surf.get_rect()[2], 10])


        else:
            pygame.draw.rect(_screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
            pygame.draw.rect(_screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
            _surf = self.arial.render(str(m_1), True, (255, 255, 255))
            _screen.blit(_surf, [101.5 - _surf.get_rect()[2] / 2, 26.5 - _surf.get_rect()[3] / 2])

        return _screen

    def __str__(self):
        return f"Level({self.blocks}, {self.enemies})"

    def __repr__(self):
        return f"Level({self.blocks}, {self.enemies})"


debug = False


size = [500, 400]

level = Level([Block([300, 150]), Block([300, 50])], [Enemy_1([150, 150]), Enemy_2([200, 200])])

done = False

while not done:
    _screen = pygame.display.set_mode(size)
    _screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if debug:
                print(level)
            done = True
        if debug:
            if event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                if event.button == 4:
                    m_1 += 30
                elif event.button == 5:
                    m_1 -= 30
                elif event.button == 1 and keys[pygame.K_1]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Block([0, 0]).size
                    level.blocks.append(Block([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))
                elif event.button == 1 and keys[pygame.K_2]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Enemy_1([0, 0]).size
                    level.enemies.append(Enemy_1([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))
                elif event.button == 1 and keys[pygame.K_3]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Enemy_2([0, 0]).size
                    level.enemies.append(Enemy_2([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))

        else:
            level.handle_event(event)

    level.update()
    _screen = level.draw(_screen)

    pygame.display.flip()
    clock.tick(30)
