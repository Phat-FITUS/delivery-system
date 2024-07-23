import pygame

class Component:
    def __init__(self) -> None:
        pass

    def isClicked(self, rect: pygame.Rect) -> bool:
        pos = pygame.mouse.get_pos()

        if rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

        if pygame.mouse.get_pressed()[0] == 0:
            return False

        return False

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        pass