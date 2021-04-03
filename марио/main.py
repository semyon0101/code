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
        _screen.blit(self.surf, (self.pos[0]-margin,self.pos[1]))
        return _screen


class Player:
    def __init__(self):
        self.surf = pygame.Surface((30, 100))
        self.pos = [100, 200]
        self.pulse_up = 0
        self.col_jump = 0
        self.max_col_jump = 2
        self.margin = 0

    def handle_event(self, _event, _blocks):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_w and self.col_jump < self.max_col_jump:
                self.pulse_up = 5
                self.col_jump += 1

    def update(self, _blocks):
        self.pulse_up -= 0.1
        self.pos[1] -= self.pulse_up

        colloid = [False, False, False, False]
        for block in _blocks:
            rect_2 = pygame.Rect(block.pos[0] - self.margin, block.pos[1], block.surf.get_rect()[2]-1,  block.surf.get_rect()[3])
            if rect_2.collidepoint((self.pos[0]-1, self.pos[1]+self.surf.get_rect()[3])) or\
               rect_2.collidepoint((self.pos[0]+self.surf.get_rect()[2]-1, self.pos[1]+self.surf.get_rect()[3])):
                colloid[1] = True
                self.pos[1] = block.pos[1] - self.surf.get_rect()[3]+1
                self.pulse_up = -self.pulse_up * 0.4
                self.col_jump = 0

            if rect_2.collidepoint((self.pos[0]-1, self.pos[1])) or rect_2.collidepoint((self.pos[0]+self.surf.get_rect()[2]-1, self.pos[1])):
                colloid[0] = True
                self.pulse_up = 0
                self.pos[1] = rect_2[3]+rect_2[1]

            if rect_2.collidepoint((self.pos[0]-1, self.pos[1])) or \
               rect_2.collidepoint((self.pos[0] - 1, self.pos[1]+self.surf.get_rect()[3]/2)) or \
               rect_2.collidepoint((self.pos[0]-1, self.pos[1]+self.surf.get_rect()[3])):
                colloid[2] = True
                self.pos[0] = block.pos[0] - self.margin + block.surf.get_rect()[2]

            if rect_2.collidepoint((self.pos[0]+self.surf.get_rect()[2]+1, self.pos[1]+1)) or \
               rect_2.collidepoint((self.pos[0]+self.surf.get_rect()[2]+1, self.pos[1]+self.surf.get_rect()[3]/2)) or \
               rect_2.collidepoint((self.pos[0]+self.surf.get_rect()[2]+1, self.pos[1]+self.surf.get_rect()[3]-1)):
                colloid[3] = True
                self.pos[0] = block.pos[0] - self.margin - self.surf.get_rect()[2]






        # print(colloid)

        if self.pos[1] > 200:
            self.pos[1] = 200
            self.pulse_up = -self.pulse_up * 0.4
            self.col_jump = 0


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not colloid[2]:
            if self.pos[0] <= 100:
                self.margin -= 5
            else:
                self.pos[0] -= 5
        elif keys[pygame.K_d] and not colloid[3]:
            if self.pos[0] >= 400:
                self.margin += 5
            else:
                self.pos[0] += 5

    def draw(self, _screen):
        _screen.blit(self.surf, self.pos)
        return _screen


player = Player()
blocks = [Block([300, 150])]

ground = pygame.Surface((500, 100))
ground.fill((40, 200, 10))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        player.handle_event(event, blocks)
    screen.fill((30, 30, 30))
    player.update(blocks)

    screen = player.draw(screen)
    screen = blocks[0].draw(screen, player.margin)

    screen.blit(ground, (0, 300))
    pygame.display.flip()
    clock.tick(30)
