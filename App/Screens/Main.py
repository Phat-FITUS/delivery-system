from .Screen import Screen
from ..Constant import Color
from ..Components import Button
from .Levels import LevelScreen
from ..External import Level_1, Level_2, Level_3, Level_4
import pygame

class Main(Screen):
    def __init__(self, *args) -> None:
        super(Main, self).__init__(*args)
        self.btn_lv1 = Button.ImageButton("./Assets/lv1.png", 0.5)
        self.btn_lv2 = Button.ImageButton("./Assets/lv2.png", 0.5)
        self.btn_lv3 = Button.ImageButton("./Assets/lv3.png", 0.5)
        self.btn_lv4 = Button.ImageButton("./Assets/lv4.png", 0.5)

    def handleLevel(self, level: int) -> callable:
        if (level == 1):
            lv = Level_1("./Test/level1/input_1.txt")
        elif (level == 2):
            lv = Level_2("./Test/level2/input_3.txt")
        elif (level == 3):
            lv = Level_3("./input1_level3.txt")
        elif (level == 4):
            lv = Level_4("./input1_level4.txt")

        def handle() -> None:
            app = LevelScreen(lv, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font)
            app.run()

        return handle

    def run(self) -> None:
        while self.running:
            self.drawBackground()
            self.displayText("MAIN MENU", self.font, Color.WHITE, self.SCREEN_WIDTH // 2, 100)

            self.btn_lv1.draw(self.screen, self.SCREEN_WIDTH // 2, 170, self.handleLevel(1))
            self.btn_lv2.draw(self.screen, self.SCREEN_WIDTH // 2, 240, self.handleLevel(2))
            self.btn_lv3.draw(self.screen, self.SCREEN_WIDTH // 2, 310, self.handleLevel(3))
            self.btn_lv4.draw(self.screen, self.SCREEN_WIDTH // 2, 380, self.handleLevel(4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()