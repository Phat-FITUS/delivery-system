from .Screen import Screen
from ..Constant import Color
import pygame

class Main(Screen):
    def __init__(self, *args) -> None:
        super(Main, self).__init__(*args)

    def run(self) -> None:
        while self.running:
            self.drawBackground()
            self.displayText("MAIN MENU", self.font, Color.WHITE, self.SCREEN_WIDTH // 2, 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()