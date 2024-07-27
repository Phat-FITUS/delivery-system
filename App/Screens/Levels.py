import pygame
from .Screen import Screen
from ..Constant import Color
from ..External import Level, Level_1, Astar, UCS, GBFS, BFS, DFS
from ..Components import Button
import time

class LevelScreen(Screen):
    def __init__(self, level: Level, *args) -> None:
        super(LevelScreen, self).__init__(*args)
        self.cell_size = 50
        self.level = level
        self.search = Astar(level)

        self.grid_w = self.level.n * self.cell_size
        self.grid_h = self.level.m * self.cell_size

        self.state = 0
        self.fuel = self.level.f
        self.finish = False

        self.btn_astar = Button.ImageButton("./Assets/asao.png", 0.25)
        self.btn_ucs = Button.ImageButton("./Assets/ucs.png", 0.25)
        self.btn_gbfs = Button.ImageButton("./Assets/gbfs.png", 0.25)
        self.btn_bfs = Button.ImageButton("./Assets/bfs.png", 0.25)
        self.btn_dfs = Button.ImageButton("./Assets/dfs.png", 0.25)
    
        self.path = self.search.run()

    def drawRect(self, x: int, y: int, color: tuple, colorMode: int = 0) -> None:
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect, colorMode)

    def drawTextCell(self, text: str, x: int, y: int, txt_color: tuple, bg_color: tuple) -> None:
        self.drawRect(x, y, bg_color)
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

        text = self.font.render(text, True, txt_color)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def drawCell(self, value: int, x: int, y: int) -> None:
        if value == 0:
            self.drawRect(x, y, Color.WHITE, 1)
        elif value == -1:
            self.drawRect(x, y, Color.DARK_BLUE)
        else:
            self.drawTextCell(str(value), x, y, Color.BLACK, Color.WHITE)

    def drawStartGoal(self, start_x: int, start_y: int) -> None:
        start_num = len(self.level.agents.values())
        index = 1
        goal_num = len(self.level.agents.values())
        
        path = self.path

        for start_pos in self.level.agents.values():
            x, y = start_pos.start
            self.drawTextCell("S" if start_num == 1 else f"S{index}", start_x + x * self.cell_size, start_y + y * self.cell_size, Color.WHITE, Color.DARK_GREEN)

            x, y = start_pos.goal[0]
            self.drawTextCell("G" if goal_num == 1 else f"G{index}", start_x + x * self.cell_size, start_y + y * self.cell_size, Color.WHITE, Color.LIGHT_RED)
            index += 1

    def drawPath(self, start_x: int, start_y: int):
        path = self.path
        if path is None:
            return

        path = path[1:-1]
        for pos in path:
            if pos[1] < self.state:
                y, x = pos[0][0]
                x = start_x + x * self.cell_size
                y = start_y + y * self.cell_size
                self.drawRect(x, y, Color.YELLOW)
            elif pos[1] == self.state:
                self.fuel -= self.search.history[pos]['fuel'][pos[0][0]]
                y, x = pos[0][0]
                x = start_x + x * self.cell_size
                y = start_y + y * self.cell_size
                self.drawRect(x, y, Color.PURPLE)

        if self.state > path[-1][1]:
            self.finish = True

    def drawGrid(self, start_x: int, start_y: int):
        end_x = start_x + self.grid_w
        end_y = start_y + self.grid_h

        self.drawStartGoal(start_x, start_y)
        self.drawPath(start_x, start_y)
    
        for x in range (start_x, end_x, self.cell_size):
            for y in range (start_y, end_y, self.cell_size):
                pos_x = (x - start_x) // self.cell_size
                pos_y = (y - start_y) // self.cell_size
                
                self.drawCell(self.level.map[pos_y][pos_x].value, x, y)


    def drawLayout(self) -> None:
        self.drawBackground()
        self.drawGrid(50, 50)
        self.displayText(f"State: {self.state}", self.font, Color.WHITE, 200, 600)
        self.displayText(f"Fuel: {self.fuel}", self.font, Color.WHITE, 200, 650)

        if isinstance(self.level, Level_1):
            self.btn_astar.draw(self.screen, 800, 50, self.handleSearch(0))
            self.btn_ucs.draw(self.screen, 800, 150, self.handleSearch(1))
            self.btn_gbfs.draw(self.screen, 800, 250, self.handleSearch(2))
            self.btn_bfs.draw(self.screen, 800, 350, self.handleSearch(3))
            self.btn_dfs.draw(self.screen, 800, 450, self.handleSearch(4))

    def handleSearch(self, algo: int) -> callable:
        if algo == 0:
            search_algo = Astar(self.level)
        elif algo == 1:
            search_algo = UCS(self.level)
        elif algo == 2:
            search_algo = GBFS(self.level)
        elif algo == 3:
            search_algo = BFS(self.level)
        elif algo == 4:
            search_algo = DFS(self.level)

        def search():
            self.search = search_algo
            self.search.run()
            self.state = 0
            self.fuel = self.level.f
            self.finish = False

        return search

    def run(self) -> None:
        while self.running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    self.running = False

            self.drawLayout()

            pygame.display.update()

            if not self.finish:
                time.sleep(1)
                self.state += 1