import pygame


class Game_clock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.clock_font = pygame.font.SysFont(None, 36)
        self.game_clock = pygame.time.Clock()
        self.clock_surface = pygame.Surface((100, 32))
        self.clock_surface.fill(pygame.Color('dodgerblue1'))
        self.rect = self.clock_surface.get_rect(topleft=(800, 20))
        self.gc = "00:00"
        self.text_surface = self.clock_font.render(self.gc, True, (0,0,0))
        self.text_rect = self.text_surface.get_rect()
        self.clock_surface.blit(self.text_surface, self.text_rect)
        
        self.z = 0

        self.image = self.clock_surface
    
    def tick(self):
        self.z = self.z + self.game_clock.tick(60)
        peepee = self.z / 1000
        self.gc = str(peepee)
        self.clock_surface = pygame.Surface((100, 32))
        self.clock_surface.fill(pygame.Color('dodgerblue1'))
        self.text_surface = self.clock_font.render(self.gc, True, (0,0,0)) 
        self.clock_surface.blit(self.text_surface, self.text_rect)

        self.image = self.clock_surface


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("Clock!")