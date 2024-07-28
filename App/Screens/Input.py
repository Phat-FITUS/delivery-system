from .Screen import Screen
from ..Constant import Color
from ..Components import Button
from .Levels import LevelScreen
from ..External import Level_1, Level_2, Level_3, Level_4
import pygame

class InputScreen(Screen):
    def __init__(self, levelName: str, *args) -> None:
        super(InputScreen, self).__init__(*args)
        self.btn_inp1 = Button.ImageButton("./Assets/input1.png", 0.25)
        self.btn_inp2 = Button.ImageButton("./Assets/input2.png", 0.25)
        self.btn_inp3 = Button.ImageButton("./Assets/input3.png", 0.25)
        self.btn_inp4 = Button.ImageButton("./Assets/input4.png", 0.25)
        self.btn_inp5 = Button.ImageButton("./Assets/input5.png", 0.25)

        self.levelName = levelName

    def getLevel(self, level:str, inpfile: str) -> str:
        if level == "level1":
            return Level_1(f"./{inpfile}_{level}.txt")
        elif level == "level2":
            return Level_2(f"./{inpfile}_{level}.txt")
        elif level == "level3":
            return Level_3(f"./{inpfile}_{level}.txt")
        elif level == "level4":
            return Level_4(f"./{inpfile}_{level}.txt")
        else:
            return ""
    
    def handleInput(self, input: int) -> callable:
        def handle() -> None:
            if input == 1:
                level = self.getLevel(self.levelName, "input1")
                outputName = f"./output1_{self.levelName}.txt"
            elif input == 2:
                level = self.getLevel(self.levelName, "input2")
                outputName = f"./output2_{self.levelName}.txt"
            elif input == 3:
                level = self.getLevel(self.levelName, "input3")
                outputName = f"./output3_{self.levelName}.txt"
            elif input == 4:
                level = self.getLevel(self.levelName, "input4")
                outputName = f"./output4_{self.levelName}.txt"
            elif input == 5:
                level = self.getLevel(self.levelName, "input5")
                outputName = f"./output5_{self.levelName}.txt"

            app = LevelScreen(level, outputName, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font)
            app.run()

        return handle

    def run(self) -> None:
        while self.running:
            self.drawBackground()
            self.displayText("CHOOSE INPUT", self.font, Color.WHITE, self.SCREEN_WIDTH // 2 - 200, 100)

            self.btn_inp1.draw(self.screen, self.SCREEN_WIDTH // 2 - 200, 170, self.handleInput(1))
            self.btn_inp2.draw(self.screen, self.SCREEN_WIDTH // 2 - 200, 240, self.handleInput(2))
            self.btn_inp3.draw(self.screen, self.SCREEN_WIDTH // 2 - 200, 310, self.handleInput(3))
            self.btn_inp4.draw(self.screen, self.SCREEN_WIDTH // 2 - 200, 380, self.handleInput(4))
            self.btn_inp5.draw(self.screen, self.SCREEN_WIDTH // 2 - 200, 450, self.handleInput(5))

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    self.running = False

            pygame.display.update()