from scripts.custom_sprites import AnimatedSprite, AnimationSequence

class Tardigrade(AnimatedSprite):
    def __init():
        seq0 = AnimationSequence(
            images_d[(0, 0)],
            images_d[(1, 0)],
            images_d[(2, 0)],
            images_d[(3, 0)],
        )
        seq1 = AnimationSequence(
            images_d[(0, 1)],
            images_d[(1, 1)],
            images_d[(2, 1)],
            images_d[(3, 1)],
        )
        seq2 = AnimationSequence(
            images_d[(0, 2)],
            images_d[(1, 2)],
            images_d[(2, 2)],
            images_d[(3, 2)],
        )
        seq3 = AnimationSequence(
            images_d[(0, 3)],
            images_d[(1, 3)],
            images_d[(2, 3)],
            images_d[(3, 3)],
        )

        super().__init__(
        {"0": seq0, "1": seq1, "2": seq2, "3": seq3},
        Vector2(100, 100),
        units,
        render_layers["active"],
        anchor="center",
        offset=Vector2(0, 10),
        )