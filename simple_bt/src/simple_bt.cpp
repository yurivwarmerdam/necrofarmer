#include "simple_bt.h"
#include <behaviortree_cpp/tree_node.h>
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <thread>

namespace py = pybind11;

BT::NodeStatus ApproachObject::tick() {
  std::cout << "approach object: " << this->name() << std::endl;

  std::this_thread::sleep_for(5s);
  return BT::NodeStatus::SUCCESS;
}

BT::NodeStatus CheckBattery() {
  std::cout << "Battery OK" << std::endl;
  return BT::NodeStatus::SUCCESS;
}

BT::NodeStatus GripperInterface::open() {
  std::cout << "open" << std::endl;
  _open = true;
  return BT::NodeStatus::SUCCESS;
}
BT::NodeStatus GripperInterface::close() {
  std::cout << "close" << std::endl;
  _open = false;
  return BT::NodeStatus::SUCCESS;
}

int simple_run() {
  std::cout << "testing" << std::endl;
  // Fairly sure this is an overview of different ways in wich you can
  // call/organize/define your nodes/actions.
  BT::BehaviorTreeFactory factory;
  factory.registerNodeType<ApproachObject>("ApproachObject");
  factory.registerSimpleCondition("CheckBattery", std::bind(CheckBattery));
  GripperInterface gripper;

  factory.registerSimpleAction("OpenGripper",
                               std::bind(&GripperInterface::open, &gripper));
  factory.registerSimpleAction("CloseGripper",
                               std::bind(&GripperInterface::close, &gripper));
  auto tree =
      factory.createTreeFromFile("/c/dev/c/btrees/simple_bt/some_tree.xml");
  tree.tickOnce();

  return 0;
}

int test_func(py::function thing) {
  thing();
  // py::gil_scoped_release release;
  std::cout << "starting" << std::endl;
  std::this_thread::sleep_for(std::chrono::milliseconds(2000));
  std::cout << "ended" << std::endl;

  return 0;
}

PYBIND11_MODULE(simple_run_bind, handle) {
  handle.doc() = "some docstring";
  handle.def("a_func", &simple_run);
  handle.def("test_func", &test_func);

  // py::class_<TreeBuilder>(handle, "PyTreeBuilder")
  //     .def(py::init<py::function, py::function, py::function>());
}

SleeperC::SleeperC(const std::string &name, const NodeConfig &config,
                   const py::function &py_func)
    : StatefulActionNode(name, config), py_func(py_func) {}

SleeperC::SleeperC(const std::string &name, const NodeConfig &config)
    : StatefulActionNode(name, config) {}

PortsList SleeperC::providedPorts() { return {}; }
BT::NodeStatus SleeperC::onStart() {
  // py::gil_scoped_release release;
  py_thread = std::thread([&]() { py_func(); });
  return BT::NodeStatus::SUCCESS;
}
BT::NodeStatus SleeperC::onRunning() { return BT::NodeStatus::SUCCESS; }
void SleeperC::onHalted() {}
SleeperC::~SleeperC() {
  // delete py_func;
  // std::thread py_thread;
}

TreeBuilder::TreeBuilder(const py::function &py_sleeper,
                         const py::function &output_dummy,
                         const py::function &parameter_sleeper) {}
void TreeBuilder::do_tree_build(const py::function &py_sleeper) {
  BT::BehaviorTreeFactory factory;
  factory.registerNodeType<SleeperC>("SleeperC", py_sleeper);
  // factory.registerNodeType<OutputDummyC, py::function>("OutputDummyC",
  //                                                      output_dummy);
  // factory.registerNodeType<ParameterSleeperC,
  // py::function>("ParameterSleeperC",
  //                                                           parameter_sleeper);
  tree = factory.createTreeFromFile("simple_bt/trees/skeleton.xml");
}
