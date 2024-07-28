import pygame

class Component:
    def __init__(self) -> None:
        self.clicked = False

    def isClicked(self, rect: pygame.Rect) -> bool:
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if rect.collidepoint(pos):
            if mouse_pressed == 1 and not self.clicked:
                self.clicked = True
                return True
            elif mouse_pressed == 0:
                self.clicked = False
                return False

        return False

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        pass