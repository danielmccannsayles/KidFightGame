import pygame

SECOND_TICK_EVENT = pygame.USEREVENT + 1
CLOCK_FONT = pygame.font.SysFont(None, 36)


class ClockWrapper(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.game_clock = pygame.time.Clock()
        self.clock_surface = pygame.Surface((100, 32))
        self.rect = self.clock_surface.get_rect(topleft=(pos))

        # State
        self.z = 0  # Elapsed time in milliseconds
        self.last_second = 0  # Last whole second value
        self.label = "00:00"
        self.paused = False

        # Start
        self.draw_face()

    def draw_face(self):
        text_surface = CLOCK_FONT.render(self.label, True, (0, 0, 0))
        text_rect = text_surface.get_rect()

        self.clock_surface.fill(pygame.Color("dodgerblue1"))
        self.clock_surface.blit(text_surface, text_rect)

        self.image = self.clock_surface

    def update(self):
        # Call tick() every time to avoid dt piling up during pause
        delta_t = self.game_clock.tick(60)
        if not self.paused:
            # Add delta, calculate total and rounded
            self.z += delta_t
            total_seconds = self.z / 1000
            rounded_second = int(total_seconds)

            # Emit event every second
            if rounded_second > self.last_second:
                self.last_second = rounded_second
                pygame.event.post(pygame.event.Event(SECOND_TICK_EVENT))

            self.label = str(total_seconds)

        self.draw_face()

    def toggle_pause(self):
        self.paused = not self.paused

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle_pause()
