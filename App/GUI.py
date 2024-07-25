import pygame
from .Screens.Main import Main

class Window:
    def __init__(self, font="./Assets/Pixel/PixelifySans-VariableFont_wght.ttf") -> None:
        pygame.init()
        self.setupAttributes(font)
        pygame.display.set_caption("Delivery system")

    def setupAttributes(self, font) -> None:
        self.SCREEN_HEIGHT = 700
        self.SCREEN_WIDTH = 1000

        self.text_font = pygame.font.Font(font, 55)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def run(self) -> None:
        app = Main(self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.text_font, "./Assets/background.jpg")
        app.run()

        pygame.quit()

if __name__ == "__main__":
    app = Window()
    app.run()