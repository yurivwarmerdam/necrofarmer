#include "simple_bt.h"
#include <behaviortree_cpp/bt_factory.h>
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
  py::gil_scoped_release release;
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
  auto tree = factory.createTreeFromFile("simple_bt/trees/some_tree.xml");
  tree.tickOnce();

  return 0;
}

int test_func(py::function thing) {
  thing();
  py::gil_scoped_release release;
  std::cout << "starting" << std::endl;
  std::this_thread::sleep_for(std::chrono::milliseconds(2000));
  std::cout << "ended" << std::endl;

  return 0;
}

SleeperC::SleeperC(const std::string &name, const NodeConfig &config,
                   const py::function &py_func)
    : StatefulActionNode(name, config), py_func(py_func) {}

SleeperC::SleeperC(const std::string &name, const NodeConfig &config)
    : StatefulActionNode(name, config) {}

PortsList SleeperC::providedPorts() { return {}; }

BT::NodeStatus SleeperC::onStart() {
  // std::future<void> py_future = std::async(std::launch::async, py_func);
  done = false;

  py_thread = std::thread([&]() {
    py_func();
    done = true;
  });
  return BT::NodeStatus::SUCCESS;
}
BT::NodeStatus SleeperC::onRunning() {
  if (done) {
    return BT::NodeStatus::SUCCESS;
  } else {
    return BT::NodeStatus::RUNNING;
  }
}
void SleeperC::onHalted() {}
SleeperC::~SleeperC() {
  // delete py_func;
  // std::thread py_thread;
}

TreeBuilder::TreeBuilder(const py::function &py_sleeper,
                         const py::function &output_dummy,
                         const py::function &parameter_sleeper) {

  factory.registerNodeType<SleeperC>("SleeperC", py_sleeper);
  // factory.registerNodeType<OutputDummyC, py::function>("OutputDummyC",
  //                                                      output_dummy);
  // factory.registerNodeType<ParameterSleeperC,
  // py::function>("ParameterSleeperC",
  //                                                           parameter_sleeper);
}

// TODO: Got dammit. Trees are @brief...! They go out of scope, they are
// destroyed. Time to think THIS nonsense over
void TreeBuilder::tick_tree() {
  Tree tree = factory.createTreeFromFile("simple_bt/trees/skeleton.xml");
  tree.tickOnce();
}

PYBIND11_MODULE(simple_run_bind, handle) {
  handle.doc() = "some docstring";
  handle.def("simple_run", &simple_run);
  handle.def("test_func", &test_func);

  py::class_<TreeBuilder>(handle, "PyTreeBuilder")
      .def(py::init<py::function, py::function, py::function>())
      .def("tick_tree", &TreeBuilder::tick_tree);
}
