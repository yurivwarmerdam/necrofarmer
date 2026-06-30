from scripts.behaviortree_py.behaviortree import (
    BehaviorTreeFactory,
    NodeStatus,
    SimpleActionNode,
)
from scripts.behaviortree_py import base_nodes


def main():
    blackboard = {}
    nodes = {
        "Succeeder": base_nodes.Succeeder,
        "Failer": base_nodes.Failer,
        "Outputter": base_nodes.Outputter,
        "Talker": base_nodes.Talker,
        "HaveBlackboardEntry": base_nodes.HaveBlackboardEntry,
    }

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
    main_tree = factory.load_tree_from_xml("scripts/behaviortree_py/demo_trees/fallback_tree.xml")
    late_talker_tree = factory.load_tree_from_xml("scripts/behaviortree_py/demo_trees/late_tree.xml")

    print("initial tick")
    tree_status = main_tree.tick()
    # while True:
    while tree_status == NodeStatus.RUNNING:
        # print("ticking")
        print(f"Tree status: {tree_status}")
        tree_status = main_tree.tick()

    print("-------")
    main_tree.tick()
    main_tree.tick()
    print(f"Once more: {tree_status}")
    while tree_status == NodeStatus.RUNNING:
        # print("ticking")
        print(f"Tree status: {tree_status}")
        tree_status = main_tree.tick()


if __name__ == "__main__":
    main()
