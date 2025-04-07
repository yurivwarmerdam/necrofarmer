from enum import Enum


class NodeStatus(Enum):
    IDLE = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    SKIPPED = 4


class BehaviorTreePy:
    """Entry point for creating and running trees."""

    # Perhaps just load tree in constructor?
    def load_tree():
        pass

    def load_blackboard():
        pass

    def tick_tree():
        pass


class Node:
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

    pass


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

    def reset_children(self):
        for child in self.children:
            child.status = NodeStatus.IDLE


class FallBackNode(ControlNode):
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
                        self.node_status = NodeStatus.IDLE
                        return NodeStatus.FAILURE
                    else:
                        self.current_node += 1
                        return NodeStatus.RUNNING
                case NodeStatus.SUCCESS:
                    self.current_node = 0
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
    """Stateful action node that keeps track of the process it is responsible for,"""


class InputPort:
    def get() -> any:
        pass


class StaticInputPort(InputPort):
    """Allows nodes to transparently read input port values.

    Args:
        value: the value contained within this Port.
    """
    def __init__(self, value):
        self.value = value

    def get(self) -> any:
        return self.value


class BBInputPort(InputPort):
    """Allows nodes to transparently read input port values from the global blackboard.

    Args:
        blackboard: the blackboard to real values from.
        key: the the blackboard key containing the relevant port value.
    """
    def __init__(self, blackboard:dict, key:str):
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
    def __init__(self, blackboard:dict, key:str):
        self.blackboard = blackboard
        self.key = key

    def set(self, value):
        self.blackboard[self.key] = value
