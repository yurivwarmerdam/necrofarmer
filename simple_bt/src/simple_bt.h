#include "behaviortree_cpp/action_node.h"
#include "behaviortree_cpp/bt_factory.h"
#include <behaviortree_cpp/basic_types.h>
#include <behaviortree_cpp/tree_node.h>
#include <chrono>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <string>

namespace py = pybind11;

using namespace std::chrono_literals;
using namespace BT;
using std::string;

class ApproachObject : public BT::SyncActionNode {
public:
  explicit ApproachObject(const string &name) : SyncActionNode(name, {}) {}
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

class SleeperC : public BT::StatefulActionNode {
public:
  SleeperC(const std::string &name, const NodeConfig &config,
           const py::function &py_func);
  SleeperC(const std::string &name, const NodeConfig &config);
 
  static BT::PortsList providedPorts();
  ~SleeperC();
  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;
private:
  py::function py_func;
  std::thread py_thread;
};

class OutputDummyC : public StatefulActionNode {
public:
  OutputDummyC(const std::string &name, const NodeConfig &config,
               const py::function &py_func);
  static BT::PortsList providedPorts();

  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  py::function py_func;
  std::thread py_thread;
};

class ParameterSleeperC : public StatefulActionNode {
public:
  ParameterSleeperC(const std::string &name, const NodeConfig &config,
                    const py::function &py_func);
  static BT::PortsList providedPorts();
  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  py::function py_func;
  std::thread py_thread;
};

class TreeBuilder {
public:
  TreeBuilder(const py::function &sleeper, const py::function &output_dummy,
              const py::function &parameter_sleeper);

  Tree GetTree();
  void do_tree_build(const py::function &py_sleeper);
private:
  py::function sleeper;
  py::function output_dummy;
  py::function parameter_sleeper;
  Tree tree;
};