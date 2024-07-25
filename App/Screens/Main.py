from .Screen import Screen
from ..Constant import Color
from ..Components import Button
from .Levels import LevelScreen
from ..External import Level_1, Level_2, Level_3
import pygame

class Main(Screen):
    def __init__(self, *args) -> None:
        super(Main, self).__init__(*args)
        self.btn_lv1 = Button.ImageButton("./Assets/lv1.png", 0.5)
        self.btn_lv2 = Button.ImageButton("./Assets/lv2.png", 0.5)
        self.btn_lv3 = Button.ImageButton("./Assets/lv3.png", 0.5)
        self.btn_lv4 = Button.ImageButton("./Assets/lv4.png", 0.5)

    def handleLevel1(self) -> None:
        lv = Level_1("./input1_level1.txt")
        app = LevelScreen(lv, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font)
        app.run()

    def handleLevel2(self) -> None:
        lv = Level_2("./input1_level2.txt")
        app = LevelScreen(lv, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font)
        app.run()

    def handleLevel3(self) -> None:
        lv = Level_3("./input1_level3.txt")
        app = LevelScreen(lv, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font)
        app.run()

    def handleLevel4(self) -> None:
        pass

    def run(self) -> None:
        while self.running:
            self.drawBackground()
            self.displayText("MAIN MENU", self.font, Color.WHITE, self.SCREEN_WIDTH // 2, 100)

            self.btn_lv1.draw(self.screen, self.SCREEN_WIDTH // 2, 170, self.handleLevel1)
            self.btn_lv2.draw(self.screen, self.SCREEN_WIDTH // 2, 240, self.handleLevel2)
            self.btn_lv3.draw(self.screen, self.SCREEN_WIDTH // 2, 310, self.handleLevel3)
            self.btn_lv4.draw(self.screen, self.SCREEN_WIDTH // 2, 380, self.handleLevel4)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()