from scripts.behaviortree_py.behaviortree import ControlNode, DecoratorNode, LeafNode, NodeStatus




class InverterNode(DecoratorNode):
    """Inverter node. Returns failure when child succeds, and the reverse.
    Otherwise passes the child's status"""

    def tick(self) -> NodeStatus:
        self.node_status = self.child.tick()
        match self.node_status:
            case NodeStatus.SUCCESS:
                self.node_status = NodeStatus.FAILURE
                self.reset_child()
                return self.node_status
            case NodeStatus.FAILURE:
                self.node_status = NodeStatus.SUCCESS
                self.reset_child()
                return self.node_status
            case _:
                return self.node_status

    def reset_child(self):
        self.child.node_status = NodeStatus.IDLE


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
                    print(
                        f"This should be an error! Child  {self.children[self.current_node]} state is: {child_status}"
                    )
                    return NodeStatus.FAILURE


class FallbackNode(ControlNode):
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


class ReactiveSequenceNode(SequenceNode):
    """Ticks first child every tick. Behaves like a regular Sequence for the other children.
    First child should always return success or failure. This node will log en error if it returns something else."""

    def tick(self):
        if self.current_node == 0:
            self.current_node += 1

        reactive_status = self.children[0].tick()
        match reactive_status:
            case NodeStatus.FAILURE:
                self.reset_children()
                self.current_node = 0
                self.node_status = NodeStatus.IDLE
                return NodeStatus.FAILURE
            case NodeStatus.SUCCESS:
                return super().tick()
            case _:
                print(
                    f"This should be an error! Reactive child state is: {reactive_status}"
                )
                return NodeStatus.FAILURE

    pass


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