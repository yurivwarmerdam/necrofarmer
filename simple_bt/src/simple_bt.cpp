#include "simple_bt.h"
#include <chrono>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <thread>

namespace py = pybind11;

struct SkeletonActions {
  py::function wait;
  py::function walk_toward_player;

public:
  SkeletonActions
};

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
  py::gil_scoped_release release;
  std::cout << "starting" << std::endl;
  std::this_thread::sleep_for(std::chrono::milliseconds(2000));
  std::cout << "ended" << std::endl;

  return 0;
}

class SkeletonAI {
  SkeletonActions actions;
public:
  SkeletonAI(py::function wait, py::function walk_toward_player) {
    actions.wait = wait;
    actions.walk_toward_player = walk_toward_player;
  }
};

// this does... nothing? Because it's not referenced in the cmake.
PYBIND11_MODULE(bind, handle) { handle.def("asd", &test_func); }

PYBIND11_MODULE(simple_run_bind, handle) {
  handle.doc() = "some docstring";
  handle.def("a_func", &simple_run);
  handle.def("test_func", &test_func);
}
