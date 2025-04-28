from pygame.math import Vector2
from pygame import Surface
from pygame.key import ScancodeWrapper
from scripts.entities import Seed
from pygame.sprite import Sprite

class PlayerEntity:
    def __init__(self, game, e_type, pos, size, sprite, mana=200):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.sprite = sprite
        self.size = size
        self.velocity = Vector2(0, 0)
        self.mana = mana

    def update(self, delta: float, input_movement: Vector2, keys: ScancodeWrapper):
        frame_movement = input_movement + self.velocity
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.mana += 1 * delta
        self.mana = min(self.mana, 200)

    def render(self, surface: Surface):
        surface.blit(self.sprite, self.pos)

    def action(self):
        if self.mana >= 50:
            self.spawn_seed()
            self.mana -= 50

    def spawn_seed(self):
        self.game.seeds.add(
            Seed(self, self.game.assets["seed"], self.game.player.pos),
        )


class JobCoordinator:
    #TODO: decide on proper naming of task vs interactible. Maybe object and task? Which to use where? dunno.

    def __init__(self,player:PlayerEntity):
        self.player=player
        self.handled_jobs=[]

    def get_possible_jobs(self):
        self.get_interactibles()



    def get_interactibles(self):
        #do a collider check for all Sprites with an "interactible" collider
        interactibles=[]
        return [item for item in interactibles if item not in self.handled_jobs]
    
    def get_idle_skeletons(self):
        # ask all skeletons if actionstatus is idle
        # return the ones where blackboard[action_status]==ACTION_STATUS.IDLE
        pass

    def give_task(self,task_type:str,interactible:Sprite):
        skeletons=self.get_idle_skeletons()
        # could become closest to job
        skeleton=skeletons(0)
        skeleton.give_task(task_type)
        #this should set skeleton.blackboard[central_job]=(task,interactible)
        self.handled_jobs.append(interactible)

    def handle_cancelled_task(task):
