import ast

from enum import Enum
from abc import ABC
from typing import Callable, Type
from bs4 import BeautifulSoup as soup


class NodeStatus(Enum):
    IDLE = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    SKIPPED = 4


class Node(ABC):
    """Basic node type."""

    def __init__(self):
        self.node_status = NodeStatus.IDLE

    def tick(self) -> NodeStatus:
        pass


class ControlNode(Node):
    """Template class for any non-leaf nodes."""

    def __init__(self, children):
        super().__init__()
        self.children: list[Node] = children
        self.current_node = 0

    def tick(self) -> NodeStatus:
        """Demo-like template behavior. Not really intended to be called."""
        return self.children(self.current_node).tick()

    def reset_children(self):
        for child in self.children:
            child.node_status = NodeStatus.IDLE


class SequenceNode(ControlNode):
    def tick(self) -> NodeStatus:
        if self.node_status == NodeStatus.IDLE:
            self.node_status = NodeStatus.RUNNING
            self.current_node = 0
            return self.node_status
        elif self.node_status == NodeStatus.RUNNING:
            child_status = self.children[self.current_node].tick()
            match child_status:
                case NodeStatus.RUNNING:
                    return NodeStatus.RUNNING
                case NodeStatus.SUCCESS:
                    if self.current_node + 1 == len(self.children):
                        self.reset_children()
                        self.current_node = 0
                        self.node_status = NodeStatus.IDLE
                        return NodeStatus.SUCCESS
                    else:
                        self.current_node += 1
                        return NodeStatus.RUNNING
                case NodeStatus.FAILURE:
                    self.reset_children()
                    self.current_node = 0
                    self.node_status = NodeStatus.IDLE
                    return NodeStatus.FAILURE
                case _:
                    print(f"This should be an error! Child state is: {child_status}")
                    return NodeStatus.FAILURE


class FallbackNode(ControlNode):
    def tick(self):
        if self.node_status == NodeStatus.IDLE:
            self.node_status = NodeStatus.RUNNING
            self.current_node = 0
            return self.node_status
        elif self.node_status == NodeStatus.RUNNING:
            child_status = self.children[self.current_node].tick()
            match child_status:
                case NodeStatus.RUNNING:
                    return NodeStatus.RUNNING
                case NodeStatus.FAILURE:
                    if self.current_node + 1 == len(self.children):
                        self.current_node = 0
                        self.reset_children()
                        self.node_status = NodeStatus.IDLE
                        return NodeStatus.FAILURE
                    else:
                        self.current_node += 1
                        return NodeStatus.RUNNING
                case NodeStatus.SUCCESS:
                    self.current_node = 0
                    self.reset_children()
                    self.node_status = NodeStatus.IDLE
                    return NodeStatus.SUCCESS


class LeafNode(Node):
    """
    Template node for leaf nodes.

     Args:
        input_ports: Dict containing name:InputPort pairs used to address input ports by name.
        output_ports: Dict containing name:Output ports used to address output ports by name.
    """

    def __init__(self, input_ports={}, output_ports={}):
        super().__init__()
        self.input_ports = input_ports
        self.output_ports = output_ports

    def tick() -> NodeStatus:
        pass

    def get_input(self, name):
        """get value for named input port. Uses internally local name."""
        return self.input_ports[name].get()

    def set_output(self, name, value):
        """set named output port to value. Uses internally local name."""
        self.output_ports[name].set(value)


class SimpleActionNode(LeafNode):
    """Simple, stateless action node. Recommended for actions that do not require internal bookkeeping."""


class StatefulActionNode(LeafNode):
    """Stateful action node that monitors the running status of a process it is responsible for,"""

    def on_start(self) -> NodeStatus:
        self.node_status = NodeStatus.RUNNING
        return self.node_status

    def on_running(self) -> NodeStatus:
        self.node_status = NodeStatus.SUCCESS
        return self.node_status

    def on_halted(self):
        self.node_status = NodeStatus.IDLE

    def tick(self) -> NodeStatus:
        match self.node_status:
            case NodeStatus.IDLE:
                return self.on_start()
            case NodeStatus.RUNNING:
                self.node_status = self.on_running()
                return self.node_status
            case _:
                return self.node_status


class InputPort:
    def get() -> any:
        pass


class StaticInputPort(InputPort):
    """Allows nodes to transparently read input port values.

    Args:
        value: the value contained within this Port.
    """

    def __init__(self, value, conversion_context: dict = {}):
        self.value = self.parse_value(value, conversion_context)

    def get(self) -> any:
        return self.value

    def parse_value(self, value, context: dict):
        print(context)
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            try:
                return eval(value, {"__builtins__": {}}, context)
            except Exception:
                return value


class BBInputPort(InputPort):
    """Allows nodes to transparently read input port values from the global blackboard.

    Args:
        blackboard: the blackboard to real values from.
        key: the the blackboard key containing the relevant port value.
    """

    def __init__(self, blackboard: dict, key: str):
        self.blackboard = blackboard
        self.key = key

    def get(self) -> any:
        return self.blackboard[self.key]


class OutputPort:
    """Maps global blackboard keys to node internal names for output ports.

    Args:
        blackboard: the blackboard to write to.
        key: the global blackboard key this will write to.

    """

    def __init__(self, blackboard: dict, key: str):
        self.blackboard = blackboard
        self.key = key

    def set(self, value):
        self.blackboard[self.key] = value


class BehaviorTreeFactory:
    def __init__(self):
        self.nodes = []
        self.blackboard = {}

    def register_blackboard(self, blackboard: dict):
        self.blackboard = blackboard

    def register_node(self, node: Callable):
        self.nodes.append(node)

    def register_nodes(self, nodes: list[Callable]):
        self.nodes += nodes

    def register_conversion_context(self, conversion_context: dict):
        self.conversion_context: dict = conversion_context

    def load_tree_from_xml(self, file: str):
        with open(file, "r") as f:
            data = f.read()
        bs_data = soup(data, "xml")
        bs_tree = bs_data.find("BehaviorTree")
        tree = self.parse_elems(bs_tree)
        return tree

    def have_node(self, node_name: str) -> bool:
        in_globals = node_name in globals()
        in_nodes = node_name not in [x.__name__ for x in self.nodes]
        return in_globals and in_nodes

    def get_elem_class(self, elem_name: str) -> Type:
        if elem_name in globals():
            return globals()[elem_name]
        elif elem_name in [x.__name__ for x in self.nodes]:
            return next(
                (node for node in self.nodes if node.__name__ == elem_name), None
            )
        else:
            raise Exception(f"Unrcognized node name: {elem_name} in tree")

    def make_port(self, elem):
        # port_class = self.get_elem_class(elem.name)
        local = elem.get("local")
        bb_key = elem.get("bb")
        value = elem.get("value")
        if value:
            return {local: StaticInputPort(value, self.conversion_context)}
        elif elem.name == "InputPort":
            return {local: BBInputPort(self.blackboard, bb_key)}
        else:
            return {local: OutputPort(self.blackboard, bb_key)}

    def parse_elems(self, elems) -> Node:
        if elems.name == "BehaviorTree":
            return self.parse_elems(next(iter(elems.find_all(recursive=False)), None))
        elem_class: Callable = self.get_elem_class(elems.name)
        if issubclass(elem_class, LeafNode):
            input_ports = iter(elems.find_all("InputPort", recursive=False))
            output_ports = iter(elems.find_all("OutputPort", recursive=False))
            input_dict = {
                k: v for port in input_ports for k, v in self.make_port(port).items()
            }

            output_dict = {
                k: v for port in output_ports for k, v in self.make_port(port).items()
            }
            return elem_class(input_ports=input_dict, output_ports=output_dict)
        elif issubclass(elem_class, ControlNode):
            children = [
                self.parse_elems(child) for child in elems.find_all(recursive=False)
            ]
            return elem_class(children)
        else:
            raise Exception(f"Unimplemented behavior for: {elems.name} in tree")
