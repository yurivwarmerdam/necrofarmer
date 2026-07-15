from abc import ABC

from pygame_gui.core.interfaces.container_interface import IContainerAndContainerLike


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
        Make sure to set elements inside context_panel of main_ui.

        context_container: context_panel container
        """
        self.portrait_id: str = portrait_id

    def update(self, _delta) -> None:
        pass
