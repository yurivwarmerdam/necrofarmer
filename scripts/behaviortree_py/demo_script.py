from scripts.behaviortree_py.factory import BehaviorTreeFactory
from scripts.behaviortree_py.behaviortree import NodeStatus
from scripts.behaviortree_py import dummy_nodes
from time import sleep

from scripts.behaviortree_py.behaviortree import Node


def main():
    blackboard = {}
    nodes = {
        "Succeeder": dummy_nodes.Succeeder,
        "Failer": dummy_nodes.Failer,
        "Outputter": dummy_nodes.Outputter,
        "Talker": dummy_nodes.Talker,
        "HaveBlackboardEntry": dummy_nodes.HaveBlackboardEntry,
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
    main_tree: Node = factory.load_tree_from_xml(
        "scripts/behaviortree_py/demo_trees/fallback_tree.xml"
    )
    late_talker_tree = factory.load_tree_from_xml(
        "scripts/behaviortree_py/demo_trees/late_tree.xml"
    )
    late_talker_tree = factory.load_tree_from_xml(
        "scripts/behaviortree_py/demo_trees/dummy_tree.xml"
    )
    
    tick_result = main_tree.tick()
    while tick_result == NodeStatus.RUNNING:
        tick_result = main_tree.tick()
        print(f"tick result: {tick_result} | Tree status: {main_tree.node_status}")
        sleep(0.2)

    print("----------")

    tick_result = late_talker_tree.tick()
    while tick_result == NodeStatus.RUNNING:
        tick_result = late_talker_tree.tick()
        print(
            f"tick result: {tick_result} | Tree status: {late_talker_tree.node_status}"
        )
        sleep(0.2)


if __name__ == "__main__":
    main()
