from abc import ABC, abstractmethod
from pygame import Vector2
from game_scripts import group_server
from game_scripts.context_panel import ContextPanel


class Selectable(ABC):
    @property
    @abstractmethod
    def context_panel(self) -> type[ContextPanel]:
        """
        returns subclass of contextpanel
        which should be instantiated when this entity is selected.
        """
