from abc import ABC, abstractmethod

from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike
from game_scripts.commander import Commander, get_commander


class ContextPanel(ABC):
    """
    Portrait gives either big image, or a series of small thumbs.
    context is contextual, based on what's selected.
    """

    def __init__(
        self,
        *,
        portrait_id: str = "default",
        context_container: IContainerAndContainerLike,
    ) -> None:
        """
        Make sure to set elements inside context_panel of game_ui.

        context_container: context_panel container
        """
        self.portrait_id: str = portrait_id
        self.commander: Commander = get_commander()

    # @abstractmethod
    # def set_context_elems(self, context_container: IContainerAndContainerLike):
    #     """
    #     set elements inside context_panel of game_ui.
    #     Note that this excludes portrait_panel.

    #     context_container: context_panel container
    #     """
    #     pass

    def update(self, _delta) -> None:
        pass
