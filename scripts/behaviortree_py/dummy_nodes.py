from scripts.behaviortree_py.behaviortree import (
    NodeStatus,
    PortsList,
)
from scripts.behaviortree_py.nodes import SimpleActionNode


class Succeeder(SimpleActionNode):
    def tick(self) -> NodeStatus:
        # print("success")
        return NodeStatus.SUCCESS


class Failer(SimpleActionNode):
    def tick(self) -> NodeStatus:
        print("Failure")
        return NodeStatus.FAILURE


class Outputter(SimpleActionNode):
    def __init__(self):
        self.ports_list = PortsList({}, {"text": str})

    def tick(self) -> NodeStatus:
        self.set_output("text", "hello world!")
        return NodeStatus.SUCCESS


class Talker(SimpleActionNode):
    def __init__(self):
        self.ports_list = PortsList({"text": str}, {})

    def tick(self) -> NodeStatus:
        message = self.get_input("text")
        print(f"I found the message: {message}")
        return NodeStatus.SUCCESS


# Generic
class HaveBlackboardEntry(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({"entry": any}, {})

    def tick(self) -> NodeStatus:
        try:
            return NodeStatus.SUCCESS
        except KeyError:
            return NodeStatus.FAILURE


class BlackboardEntryEquals(SimpleActionNode):
    def __init__(self):
        super().__init__()
        self.ports_list = PortsList({"entry": any, "value": any}, {})

    def tick(self):
        if self.get_input("entry") == self.get_input("value"):
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE
