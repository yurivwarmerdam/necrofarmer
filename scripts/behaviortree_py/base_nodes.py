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
        self.ports_list=PortsList({},{"text":str})
    def tick(self) -> NodeStatus:
        self.set_output("text", "hello world!")
        return NodeStatus.SUCCESS


class Talker(SimpleActionNode):
    def __init__(self):
        self.ports_list=PortsList({"text":str},{})
    def tick(self) -> NodeStatus:
        message = self.get_input("text")
        print(f"I found the message: {message}")
        return NodeStatus.SUCCESS
