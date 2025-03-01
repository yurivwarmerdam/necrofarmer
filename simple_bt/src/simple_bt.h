#include "behaviortree_cpp/action_node.h"
#include "behaviortree_cpp/bt_factory.h"
#include <behaviortree_cpp/basic_types.h>
#include <chrono>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>



namespace py = pybind11;

using namespace std::chrono_literals;
using std::string;

class ApproachObject : public BT::SyncActionNode
{
public:
  explicit ApproachObject(const string &name) : BT::SyncActionNode(name, {}) {}
  BT::NodeStatus tick() override;
};
BT::NodeStatus CheckBattery();

class GripperInterface
{
public:
  GripperInterface() : _open(true) {}

  BT::NodeStatus open();
  BT::NodeStatus close();

private:
  bool _open;
};

int simple_run();

struct SkeletonActions
{
  py::function wait;
  py::function pick_player_walk_goal;
  py::function walk_toward_goal;
};

class SkeletonAI
{
private:
  SkeletonActions actions;
  BT::BehaviorTreeFactory factory;

public:
  SkeletonAI(py::function wait, py::function pick_player_walk_goal,
             py::function walk_toward_goal);

  BT::NodeStatus c_wait();

  BT::NodeStatus pick_player_walk_goal();

  BT::NodeStatus walk_toward_goal();
};