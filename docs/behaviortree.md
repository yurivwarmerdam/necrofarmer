# BehaviorTree.py

Normal behavior tree rules are followed.

Trees can be ticked on some regular interval using events, but this can be set up to tick every frame if needed.

Minimal class with some behavior:

``` python
from scripts.behaviortree_py.behaviortree import BehaviorTreeFactory
from scripts.entities import ActionStatus
from scripts.behaviortree_py.dummy_nodes import Failer, Succeeder

class Some_sprite(Sprite): # using sprite, because we are in pygame. Could feasibly be anything, but I like calling tick methods through a Group.

    def __init__(self,*groups):
        super().__init__(*groups)
        ## probably image & rect shenenigans. Outside of the cope of this snippet.
        self.blackboard = {"action_status": ActionStatus.IDLE, "self": self} # minimal required set of blackboard entries.
        nodes={"Succeeder": Succeeder,
            "Failer": Failer,} #some sample nodes you'll propbably end up using anyway.
        factory= BehaviorTreeFactory()
        factory.register_blackboard(self.blackboard)
        factory.register_nodes(nodes)
        factory.register_conversion_context({"Vector2": Vector2}) # In case nonstandard datatypes are described in tree.xml, provide mappings here.
        self.tree = factory.load_tree_from_xml("trees/some_tree.xml") # where your tree is defined

def tick(self):
    self.tree.tick()
```

This class needs to be ticked in a corresponding main class:

``` python
class MainClass:
    def main(self):

    def __init__(self):
        self.BTREE_EVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.BTREE_EVENT, 250)


if __name__ == "__main__":
    MainClass().main()


```