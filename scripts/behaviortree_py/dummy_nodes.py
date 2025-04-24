from scripts.behaviortree_py.behaviortree import (
    SimpleActionNode,
    NodeStatus,
    BehaviorTreeFactory,
)


class Succeeder(SimpleActionNode):
    def tick(self) -> NodeStatus:
        print("success")
        return NodeStatus.SUCCESS


class Failer(SimpleActionNode):
    def tick(self) -> NodeStatus:
        print("Failure")
        return NodeStatus.FAILURE


class Outputter(SimpleActionNode):
    def tick(self) -> NodeStatus:
        self.set_output("text", "hello world!")
        return NodeStatus.SUCCESS


class Talker(SimpleActionNode):
    def tick(self) -> NodeStatus:
        message = self.get_input("text")
        print(f"I found the message: {message}")
        return NodeStatus.SUCCESS


def main():
    blackboard = {}
    nodes = [Succeeder, Failer, Outputter, Talker]

    # sequence
    # my_sequence = SequenceNode([succeeder(), failer()])
    # my_sequence = SequenceNode(
    #     children=[SequenceNode([Succeeder(), Succeeder()]), Failer()]
    # )

    # fallabck
    # my_sequence=FallbackNode([failer(),succeeder()])
    # my_sequence=FallbackNode([succeeder(),failer()])
    # my_sequence = FallbackNode([SequenceNode([Succeeder(), Failer()]), Failer()])

    # blackboard

    # my_sequence = SequenceNode(
    #     [Talker(input_ports={"text":StaticInputPort("a static string")})]
    # )

    # my_sequence = SequenceNode(
    #     [
    #         Outputter(output_ports={"text": OutputPort(blackboard, key="key_storage")}),
    #         Talker(input_ports={"text": BBInputPort(blackboard, "key_storage")}),
    #     ]
    # )

    factory = BehaviorTreeFactory()
    factory.register_blackboard(blackboard)
    factory.register_nodes(nodes)
    my_sequence = factory.load_tree_from_xml("simple_bt/trees/dummy_tree.xml")

    print("initial tick")
    tree_status = my_sequence.tick()
    while True:
        # while tree_status == NodeStatus.RUNNING:
        print("ticking")
        tree_status = my_sequence.tick()


if __name__ == "__main__":
    main()
