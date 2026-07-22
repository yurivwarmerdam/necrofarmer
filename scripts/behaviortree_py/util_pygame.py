from pygame.sprite import Group


class BTGroup(Group):
    def tick(self, *args, **kwargs):
        """call the tick method of every member sprite

        Group.tick(*args, **kwargs): return None

        Calls the tick method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite tick function.

        """
        for sprite in self.sprites():
            sprite.tick(*args, **kwargs)
