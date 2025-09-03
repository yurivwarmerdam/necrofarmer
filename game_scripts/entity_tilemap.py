from pygame.sprite import Group
from scripts.tilemap import Tilemap

class EntityTilemap(Tilemap):
    def __init__(self, tmx_file, group_mappings: dict[str, Group], tile_entity_mapping:dict[str,class]):
        super().__init__(tmx_file, group_mappings)

    pass