#include "simple_bt.h"
#include <behaviortree_cpp/bt_factory.h>
#include <behaviortree_cpp/tree_node.h>
#include <functional>
#include <iostream>
#include <ostream>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <thread>
#include <utility>

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

PortsList SleeperC::providedPorts() { return {}; }

void SleeperC::pyWrapper() {
  // py::gil_scoped_release release;
  py_func();
  std::cout << "finished sleeper process" << std::endl;
  done = true;
}

BT::NodeStatus SleeperC::onStart() {
  // std::future<void> py_future = std::async(std::launch::async, py_func);
  std::cout << "starting sleeper node. Also concurrenly: "<< boost::thread::hardware_concurrency()  << std::endl;
  done = false;
  boost::thread thread(&SleeperC::pyWrapper, this);
  this->py_thread = std::move(thread);
  std::cout << "succesfully started sleeper node" << std::endl;
  return BT::NodeStatus::RUNNING;
}
BT::NodeStatus SleeperC::onRunning() {
  std::cout << "running sleeper node" << std::endl;
  if (done) {
    return BT::NodeStatus::SUCCESS;
  } else {
    return BT::NodeStatus::RUNNING;
  }
}
void SleeperC::onHalted() {}
SleeperC::~SleeperC() { this->py_thread.join(); }

TreeBuilder::TreeBuilder(const py::function &py_sleeper,
                         const py::function &output_dummy,
                         const py::function &parameter_sleeper) {

  factory.registerNodeType<SleeperC>("SleeperC", py_sleeper);
  // factory.registerNodeType<OutputDummyC, py::function>("OutputDummyC",
  //                                                      output_dummy);
  // factory.registerNodeType<ParameterSleeperC,
  // py::function>("ParameterSleeperC", parameter_sleeper);
}

void TreeBuilder::tick_tree() {
  auto tree = factory.createTreeFromFile("simple_bt/trees/skeleton.xml");
  auto status = tree.tickOnce();
  std::cout << "start tick done" << std::endl;
  while (status == NodeStatus::RUNNING) {
    tree.sleep(std::chrono::milliseconds(100));
    tree.tickOnce();
  }
}

PYBIND11_MODULE(simple_run_bind, handle) {
  handle.doc() = "some docstring";
  handle.def("simple_run", &simple_run);
  handle.def("test_func", &test_func);

  py::class_<TreeBuilder>(handle, "PyTreeBuilder")
      .def(py::init<py::function, py::function, py::function>())
      .def("tick_tree", &TreeBuilder::tick_tree);
}
