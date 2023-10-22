import pygame

background_color = "#3F3F3F"

class Ghost(pygame.sprite.Sprite):
    def __init__(self, start, directions, speed, zoomRate):
        size = 150
        super(Ghost, self).__init__()
        image = pygame.image.load("assets/ghost.png").convert_alpha()
        transparency = 200
        image.fill((255, 255, 255, transparency), special_flags=pygame.BLEND_RGBA_MULT)
        self.surf = pygame.transform.scale(image, (size, size))
        self.replace_surf = pygame.Surface((size, size))
        self.replace_surf.fill(background_color)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(start)

        # Left, Right, Up , Down
        self.directions = directions
        self.speed = speed

    def update(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):
        
        if self.directions[0]:
            self.rect.move_ip(-1 * self.speed, 0)
        if self.directions[1]:
            self.rect.move_ip(1 * self.speed, 0)
        if self.directions[2]:
            self.rect.move_ip(0, -1 * self.speed)
        if self.directions[3]:
            self.rect.move_ip(0, 1 * self.speed)

        ghostOff = False

        if (self.rect.left > SCREEN_WIDTH) or (self.rect.right < 0) or (self.rect.top > SCREEN_HEIGHT) or (self.rect.bottom < 0):
            ghostOff = True

        return ghostOff

class Pumpkin(pygame.sprite.Sprite):
    def __init__(self, position, size):
        self.size = size
        super(Pumpkin, self).__init__()
        image = pygame.image.load("assets/pumpkin.png")
        self.surf = pygame.transform.scale(image, (size, size))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(position)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
class Ouija(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Ouija, self).__init__()
        image = pygame.image.load("assets/ouija.png")
        self.surf = pygame.transform.scale(image, (600, 600))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(position)

        self.letters = [[91, 285, 31, 28], [132, 270, 22, 24], [156, 254, 28, 27], [190, 245, 26, 26], [217, 237, 33, 28], [251, 229, 24, 32], [281, 231, 26, 33], [316, 230, 30, 34], [353, 232, 10, 35], [373, 236, 18, 34], [403, 246, 23, 38], [435, 257, 20, 38], [465, 267, 33, 48], [95, 345, 31, 31], [127, 327, 29, 28], [157, 313, 23, 26], [183, 297, 29, 26], [213, 288, 35, 28], [249, 278, 34, 32], [288, 276, 17, 31], [312, 279, 25, 31], [342, 281, 25, 34], [383, 293, 20, 35], [419, 306, 20, 37], [453, 320, 10, 32], [472, 341, 29, 35]]
        self.letterValues = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

