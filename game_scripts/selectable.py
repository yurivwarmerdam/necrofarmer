from abc import ABC, abstractmethod

from game_scripts.ui.ui_elements import ContextPanel


class Selectable(ABC):
    """
    I don't really know what mixins are. *butterfly meme* is this a mixin?
    """

    @property
    @abstractmethod
    def context_panel(self) -> type[ContextPanel]:
        """
        returns subclass of contextpanel
        which should be instantiated when this entity is selected.
        """
