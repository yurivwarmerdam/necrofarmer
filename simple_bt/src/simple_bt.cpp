#include "simple_bt.h"
// #include <boost/python/module.hpp>
#include <pybind11/pybind11.h>

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
  BT::BehaviorTreeFactory factory;
  factory.registerNodeType<ApproachObject>("ApproachObject");
  factory.registerSimpleCondition("CheckBattery", std::bind(CheckBattery));
  GripperInterface gripper;

  factory.registerSimpleAction("OpenGripper",
                               std::bind(&GripperInterface::open, &gripper));
  factory.registerSimpleAction("CloseGripper",
                               std::bind(&GripperInterface::close, &gripper));

  auto tree = factory.createTreeFromFile("/c/dev/c/btrees/simple_bt/some_tree.xml");
  tree.tickOnce();

  return 0;
}

// How to expose function as C. Makes it consumable by ctypes. 
// You lose class functions and all that jazz, tho. Feels like it's more for funciton calls.
extern "C" {
  int c_run(){
    return simple_run();
  }
}

float some_fn(float x, float y) {
  return x+y;
}

// PYBIND11_MODULE(some_bind, m) {
//   m.doc()="an example plugin";
//   m.def("simple_run", &simple_run);
// }


PYBIND11_MODULE(some_bind, handle){
  handle.doc() = "some docstring";
  handle.def("a_func", &simple_run);
}


// This how to do it in Boost. Boost seems p. outdated, tho.
// BOOST_PYTHON_MODULE(simple_module) {
//   using namespace boost::python;
//   def("run", simple_run);
// }
