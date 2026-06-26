from scripts.behaviortree_py.behaviortree import (
    NodeStatus,
    SimpleActionNode,
)

from scripts.behaviortree_py.behaviortree import PortsList


class Succeeder(SimpleActionNode):
    def tick(self) -> NodeStatus:
        print("success")
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
        # print(f"thyicking! {self.get_input('entry')}")
        try:
            self.get_input("entry")
            print("not excepting:", self.get_input("entry"))
            return NodeStatus.SUCCESS
        except KeyError:
            print("excepting")
            return NodeStatus.FAILURE
