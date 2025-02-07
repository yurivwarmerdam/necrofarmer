#include "behaviortree_cpp/action_node.h"
#include "behaviortree_cpp/bt_factory.h"
#include <behaviortree_cpp/basic_types.h>
#include <boost/python.hpp>
#include <chrono>
#include <iostream>

using namespace std::chrono_literals;
using std::string;

class ApproachObject : public BT::SyncActionNode {
public:
  explicit ApproachObject(const string &name) : BT::SyncActionNode(name, {}) {}
  BT::NodeStatus tick() override;
};
BT::NodeStatus CheckBattery();

class GripperInterface {
public:
  GripperInterface() : _open(true) {}

  BT::NodeStatus open();
  BT::NodeStatus close();

private:
  bool _open;
};

int simple_run();

// int main() { return 0; }