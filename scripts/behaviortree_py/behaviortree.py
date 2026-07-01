from abc import ABC, abstractmethod
import ast
from enum import Enum
from pygame.sprite import Group
from dataclasses import dataclass, field


class NodeStatus(Enum):
    IDLE = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    SKIPPED = 4


class InputPort:
    def get(self) -> any:
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


@dataclass
class PortsList:
    inputports: dict[str, type] = field(default_factory=dict)
    outputports: dict[str, type] = field(default_factory=dict)


class Node(ABC):
    """Basic node type."""

    def __init__(self):
        self.node_status = NodeStatus.IDLE

    @abstractmethod
    def tick(self) -> NodeStatus:
        pass


class DecoratorNode(Node):
    """Template class for decorators."""

    def __init__(self, child: Node):
        super().__init__()
        self.child = child
        pass


class ControlNode(Node):
    """Template class for control nodes."""

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


class LeafNode(Node):
    """
    Template node for leaf nodes.
    If any ports are used in the node, it should be set inside the __init__ method.
    Make sure to also call super()__init__() if doing so.

     Args:
        input_ports: Dict containing name:InputPort pairs used to address input ports by name.
        output_ports: Dict containing name:Output ports used to address output ports by name.
    """

    def get_ports_list(self):
        return getattr(self, "ports_list", PortsList())

    def set_ports(
        self, input_ports: dict[str, InputPort], output_ports: dict[str, OutputPort]
    ):
        self.input_ports: dict[str, InputPort] = input_ports
        self.output_ports: dict[str, OutputPort] = output_ports

    @abstractmethod
    def tick(self) -> NodeStatus:
        pass

    def get_input(self, name):
        """get value for named input port. Uses internally local name."""
        return self.input_ports[name].get()

    def set_output(self, name, value):
        """set named output port to value. Uses internally local name."""
        self.output_ports[name].set(value)


class Tree:
    def __init__(self, root_node) -> None:
        pass

    pass
