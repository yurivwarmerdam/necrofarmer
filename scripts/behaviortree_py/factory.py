from typing import Callable, Type

from bs4 import BeautifulSoup as soup

from scripts.behaviortree_py import nodes
from scripts.behaviortree_py.behaviortree import (
    BBInputPort,
    ControlNode,
    DecoratorNode,
    LeafNode,
    Node,
    OutputPort,
    StaticInputPort,
    Tree,
)


class BehaviorTreeFactory:
    def __init__(self):
        self.nodes: dict = {}
        self.blackboard: dict = {}
        self.conversion_context = {}

    def register_blackboard(self, blackboard: dict):
        self.blackboard = blackboard

    def register_node(self, name, node: Callable):
        self.nodes[name] = node

    def register_nodes(self, nodes: dict):
        self.nodes.update(nodes)

    def register_conversion_context(self, conversion_context: dict):
        self.conversion_context: dict = conversion_context

    def load_tree_from_xml(self, file: str):
        with open(file, "r") as f:
            data = f.read()
        bs_data = soup(data, "xml")
        bs_tree = bs_data.find("BehaviorTree")
        tree_nodes: ControlNode = self.parse_elems(bs_tree)  # type: ignore
        return Tree(tree_nodes)

    def get_elem_class(self, elem_name: str) -> Type:
        # if elem_name in globals():
        #     return globals()[elem_name]
        if hasattr(nodes, elem_name):
            return getattr(nodes, elem_name)
        elif elem_name in self.nodes:
            return self.nodes[elem_name]
        else:
            raise Exception(f"Unrcognized node name: {elem_name} in tree")

    def make_port(self, elem):
        local = elem.get("local")
        bb_key = elem.get("bb")
        value = elem.get("value")

        if not value and not bb_key:
            raise Exception(
                f"Illegal port declaration! No value or bb key found in elem: {elem}"
            )
        if value:
            return {local: StaticInputPort(value, self.conversion_context)}
        elif elem.name == "InputPort":
            return {local: BBInputPort(self.blackboard, bb_key)}
        elif elem.name == "OutputPort":
            return {local: OutputPort(self.blackboard, bb_key)}
        else:
            raise Exception(f"Unknown port data provided. I received: {elem}")

    def parse_elems(self, elems) -> Node:
        if elems.name == "BehaviorTree":
            return self.parse_elems(next(iter(elems.find_all(recursive=False)), None))
        elem_class = self.get_elem_class(elems.name)
        args = []
        if isinstance(elem_class, tuple):
            elem_class, *args = elem_class
        if issubclass(elem_class, LeafNode):
            new_node: LeafNode = elem_class(*args)
            ports_list = new_node.get_ports_list()

            input_dict = {}
            for key in ports_list.inputports.keys():
                input_dict.update(
                    self.make_port(elems.find("InputPort", local=key, recursive=False))
                )
            output_dict = {}
            for key in ports_list.outputports.keys():
                output_dict.update(
                    self.make_port(elems.find("OutputPort", local=key, recursive=False))
                )

            new_node.set_ports(input_dict, output_dict)
            return new_node
        elif issubclass(elem_class, ControlNode):
            children = [
                self.parse_elems(child) for child in elems.find_all(recursive=False)
            ]
            return elem_class(children)
        elif issubclass(elem_class, DecoratorNode):
            child = self.parse_elems(elems.find())
            return elem_class(child)
        else:
            raise Exception(f"Unimplemented behavior for: {elems.name} in tree")
