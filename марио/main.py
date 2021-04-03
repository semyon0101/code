import pygame

pygame.init()
pygame.display.set_caption("марио")
screen = pygame.display.set_mode((500, 400))

clock = pygame.time.Clock()


class Block:
    def __init__(self, pos: list):
        self.surf = pygame.Surface((50, 50))
        self.pos = pos

    def draw(self, _screen, margin):
        _screen.blit(self.surf, self.pos)
        return _screen


class Player:
    def __init__(self):
        self.surf = pygame.Surface((30, 100))
        self.pos = [100, 200]
        self.pulse_up = 0
        self.col_jump = 0
        self.max_col_jump = 2
        self.margin = 0

    def handle_event(self, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_SPACE and self.col_jump < self.max_col_jump:
                self.pulse_up = 5
                self.col_jump += 1

    def update(self):
        self.pulse_up -= 0.1
        self.pos[1] -= self.pulse_up
        if self.pos[1] >= 200:
            self.pos[1] = 200
            self.pulse_up = -self.pulse_up * 0.4
            self.col_jump = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.pos[0] <= 100:
                self.margin -= 5
            else:
                self.pos[0] -= 5
        elif keys[pygame.K_d]:
            if self.pos[0] >= 400:
                self.margin += 5
            else:
                self.pos[0] += 5
        print(self.pulse_up, self.pos)
        # if self.pos[1]<100:
        #    self.pos[1] = 100
        #    self.pulse_up = 0

    def draw(self, _screen):
        _screen.blit(self.surf, self.pos)
        return _screen


player = Player()
block = Block([300, 20])

ground = pygame.Surface((500, 100))
ground.fill((40, 200, 10))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        player.handle_event(event)
    screen.fill((30, 30, 30))
    player.update()

    screen = player.draw(screen)
    screen = block.draw(screen, player.margin)

    screen.blit(ground, (0, 300))
    pygame.display.flip()
    clock.tick(30)
