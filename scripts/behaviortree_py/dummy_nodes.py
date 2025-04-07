from behaviortree import (
    SimpleActionNode,
    NodeStatus,
    SequenceNode,
    OutputPort,
    FallBackNode,
    StaticInputPort,
    BBInputPort,
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
    # sequence
    # my_sequence = SequenceNode([succeeder(), failer()])
    my_sequence = SequenceNode(
        children=[SequenceNode([Succeeder(), Succeeder()]), Failer()]
    )

    blackboard = {}

    # fallabck
    # my_sequence=FallBackNode([failer(),succeeder()])
    # my_sequence=FallBackNode([succeeder(),failer()])
    # my_sequence = FallBackNode([SequenceNode([Succeeder(), Failer()]), Failer()])

    # blackboard

    # my_sequence = SequenceNode(
    #     [Talker(input_ports={"text":StaticInputPort("a static string")})]
    # )

    my_sequence = SequenceNode(
        [
            Outputter(output_ports={"text": OutputPort(blackboard, key="key_storage")}),
            Talker(input_ports={"text": BBInputPort(blackboard, "key_storage")}),
        ]
    )

    print("initial tick")
    tree_status = my_sequence.tick()
    while tree_status == NodeStatus.RUNNING:
        print("ticking")
        tree_status = my_sequence.tick()


if __name__ == "__main__":
    main()
