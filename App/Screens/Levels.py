import pygame
from .Screen import Screen
from ..Constant import Color
from ..External import Level, Level_1, Astar, UCS, GBFS, BFS, DFS
from ..Components import Button
import time
import threading

class LevelScreen(Screen):
    def __init__(self, level: Level, outputName: str, *args) -> None:
        super(LevelScreen, self).__init__(*args)
        self.cell_size = 50
        self.level = level
        self.search = Astar(level)
        self.outputName = outputName

        self.grid_w = self.level.m * self.cell_size
        self.grid_h = self.level.n * self.cell_size

        self.state = 0
        self.fuel = self.level.f
        self.finish = False

        self.btn_astar = Button.ImageButton("./Assets/asao.png", 0.25)
        self.btn_ucs = Button.ImageButton("./Assets/ucs.png", 0.25)
        self.btn_gbfs = Button.ImageButton("./Assets/gbfs.png", 0.25)
        self.btn_bfs = Button.ImageButton("./Assets/bfs.png", 0.25)
        self.btn_dfs = Button.ImageButton("./Assets/dfs.png", 0.25)
    
        self.path = None
        self.loading = True
        self.isRunning = False
        self.isSave = False

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

        for start_pos in self.level.agents.values():
            y, x = start_pos.start
            self.drawTextCell("S" if start_num == 1 else f"S{index}", start_x + x * self.cell_size, start_y + y * self.cell_size, Color.WHITE, Color.DARK_GREEN)

            y, x = start_pos.goal[0]
            self.drawTextCell("G" if goal_num == 1 else f"G{index}", start_x + x * self.cell_size, start_y + y * self.cell_size, Color.WHITE, Color.LIGHT_RED)
            index += 1

    def drawPath(self, start_x: int, start_y: int):
        path = self.path
        if path is None:
            return

        path = path[1:-1]
        for expanded in self.search.expanded:
            if expanded[1] <= self.state:
                for agent_pos in expanded[0]:
                    is_start_or_goal = False
                    for start_pos in self.level.agents.values():
                        if agent_pos == start_pos.start:
                            is_start_or_goal = True
                            break
                        if agent_pos == start_pos.goal[0]:
                            is_start_or_goal = True
                            break

                    if not is_start_or_goal:
                        y, x = agent_pos
                        x = start_x + x * self.cell_size
                        y = start_y + y * self.cell_size
                        self.drawRect(x, y, Color.GREY)

        for pos in path:
            if pos[1] < self.state:
                for agent_pos in pos[0]:
                    y, x = agent_pos
                    x = start_x + x * self.cell_size
                    y = start_y + y * self.cell_size
                    self.drawRect(x, y, Color.YELLOW)
            elif pos[1] == self.state:
                for agent_pos in pos[0]:
                    y, x = agent_pos
                    self.fuel = self.level.f - self.search.history[pos]['fuel'][agent_pos]
                    x = start_x + x * self.cell_size
                    y = start_y + y * self.cell_size
                    self.drawRect(x, y, Color.PURPLE)

        if len(path) == 0 or self.state > path[-1][1]:
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

                if self.level.map[pos_y][pos_x].fuel > 0:
                    self.drawTextCell("F1", x, y, Color.WHITE, Color.LIGHT_BLUE)
                
                self.drawCell(self.level.map[pos_y][pos_x].value, x, y)

    def drawLayout(self) -> None:
        self.drawBackground()
        self.drawGrid(50, 50)
        if self.path is not None:
            self.displayText(f"State: {self.state}", self.font, Color.WHITE, 1000, 600)
            self.displayText(f"Fuel: {self.fuel}", self.font, Color.WHITE, 1000, 650)
        else:
            self.displayText("No path found", self.font, Color.WHITE, 1000, 600)

        if isinstance(self.level, Level_1):
            self.btn_astar.draw(self.screen, 1000, 50, self.handleSearch(0))
            self.btn_ucs.draw(self.screen, 1000, 150, self.handleSearch(1))
            self.btn_gbfs.draw(self.screen, 1000, 250, self.handleSearch(2))
            self.btn_bfs.draw(self.screen, 1000, 350, self.handleSearch(3))
            self.btn_dfs.draw(self.screen, 1000, 450, self.handleSearch(4))

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
            threading.Thread(target=self.runAlgo).start()

        return search
    
    def runAlgo(self) -> None:
        self.isRunning = True
        self.loading = True
        self.path = self.search.run()
        self.state = 0
        self.fuel = self.level.f
        self.finish = False
        self.loading = False
        self.isRunning = False

        if not self.isSave:
            if isinstance(self.level, Level_1):
                astar = Astar(self.level).run()
                ucs = UCS(self.level).run()
                gbfs = GBFS(self.level).run()
                bfs = BFS(self.level).run()
                dfs = DFS(self.level).run()
                self.level.write_algorithms_paths(bfs, dfs, gbfs, ucs, astar, self.outputName)
            else:
                self.level.write_path_to_file(self.path, self.outputName)
            self.isSave = True

    def run(self) -> None:
        while self.running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    self.running = False

            if self.loading:
                self.drawBackground()
                self.displayText("Loading...", self.font, Color.WHITE, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                pygame.display.update()
                if not self.isRunning:
                    threading.Thread(target=self.runAlgo).start()
            else:
                self.drawLayout()

            pygame.display.update()

            if not self.finish and self.path is not None:
                time.sleep(1)
                self.state += 1