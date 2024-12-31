import pygame
from abc import ABC, abstractmethod
class Effect(ABC):

    @staticmethod
    @abstractmethod
    def apply(image:pygame.Surface, *parameters) -> pygame.Surface:
        ...
