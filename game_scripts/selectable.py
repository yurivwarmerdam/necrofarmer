from abc import ABC, abstractmethod

from game_scripts.context_panel import ContextPanel


class Selectable(ABC):
    @property
    @abstractmethod
    def context_panel(self) -> type[ContextPanel]:
        """
        returns subclass of contextpanel
        which should be instantiated when this entity is selected.
        """
