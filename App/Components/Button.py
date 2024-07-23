import pygame
from typing import Callable
from .Component import Component

class ImageButton(Component):
	def __init__(self, image: str, scale: float = 1) -> None:
		btn_img = pygame.image.load(image)
		btn_img = btn_img.convert_alpha()

		width = btn_img.get_width()
		height = btn_img.get_height()
		self.image = pygame.transform.scale(btn_img, (int(width * scale), int(height * scale)))

	def draw(self, screen: pygame.Surface, x: int, y: int, action: Callable) -> None:
		rect = self.image.get_rect()
		rect.topleft = (x - self.image.get_width() // 2, y)

		if self.isClicked(rect):
			action()

		screen.blit(self.image, (rect.x, rect.y))