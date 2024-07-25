import pygame
from ..Constant import Color

class Screen:
    def __init__(self, screen: pygame.Surface, height: int, width: int, font: pygame.font.Font, background:str = "") -> None:
        self.screen = screen
        self.running = True
        self.SCREEN_HEIGHT = height
        self.SCREEN_WIDTH = width

        if background:
            self.background = pygame.image.load(background)
            self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        else:
            self.background = ""
        
        self.font = font
    
    def drawBackground(self) -> None:
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(Color.BLACK)

    def displayText(self, text: str, font: pygame.font.Font, text_color: tuple, x: int, y: int) -> None:
        txt = font.render(text, True, text_color)
        text_rect = txt.get_rect(center=(x, y))
        self.screen.blit(txt, text_rect)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()