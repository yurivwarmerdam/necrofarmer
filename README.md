# pygame_tst

## Cheat sheet:
```
# Clone:
git clone --recurse-submodules git@github.com:yurivwarmerdam/simple_bt.git
# venv because miniconda cannot be used since its installation of sqlite3 conflicts witht he requirements of behaviortee.cpp
source venv/bin/activate
```

environment setup install script:
```
sudo apt install libczmq-dev libsqlite3-dev pybind11-dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Some notes:
- [pytmx](https://pytmx.readthedocs.io/en/latest/). Allows loading of tilemaps into pygame. [code snippet at this video timestamp](https://youtu.be/N6xqCwblyiw?t=4793)
- [pydew valley](https://www.youtube.com/llkwatch?v=T4IX36sP_0c) Steal this liberally

## BehaviorTree.cpp install notes:
- [behaviorTrees.cpp website](https://www.behaviortree.dev/)  
- [BehaviorTree.cpp github repo](https://github.com/BehaviorTree/BehaviorTree.CPP?tab=readme-ov-file)  

all installs have been done from source.  
### Links:

[The Hummingbird tutorial P2](https://www.youtube.com/watch?v=4PUiDmD5dkg)  
[The Hummingbird tutorial P3](https://www.youtube.com/watch?v=T_Q57-audMk)  

[Sample Project](https://github.com/BehaviorTree/btcpp_sample)

[Official Tutorials](https://www.behaviortree.dev/docs/category/tutorials-basic/)

- [General intro to BTrees](https://www.youtube.com/watch?v=DCZJUvTQV5Q)  
- [one OOP BTree implementation on pytthon](https://iq.opengenus.org/b-tree-in-python/)  
- [pytrees](https://py-trees.readthedocs.io/en/devel/introduction.html)  

### learning notes:

#### pygame
Sprite class has an inbuilt update and draw method

Can also be added to a Group, which has an update and draw method, both of which will delegate to their contents.
Groups (sprites?) also have a kill() funciton that allows the object to destroy itself
There's also the spritecollide() function, allowing for a bunch of sprites to check collision with another sprite all at once.

make everything out of boxes first:
https://www.youtube.com/watch?v=bZeHah4eg-E
(boxes are easy in this framework!)


tilemap...

3D array

coordinate calculation?

Currently looking at pybind11: https://www.youtube.com/watch?v=_5T70cAXDJ0  
Corresponding gist: https://gist.github.com/safijari/f7aec85b89906b4b90a8f33039c11263  
functors: https://www.geeksforgeeks.org/functors-in-cpp/  
The BT paper: https://arxiv.org/pdf/1709.00084  
Indian demo P3 github: https://github.com/thehummingbird/robotics_demos/blob/main/behavior_trees/grasp_place_robot_demo/bt_demo.cpp


### Cheecky generated code to peek at:
```
import threading
import time
import mymodule  # This is the compiled Pybind11 module

def my_python_function():
    print("Python function started...")
    time.sleep(1)  # Simulate work
    print("Python function finished.")

# Call the C++ function inside a Python thread
thread = threading.Thread(target=mymodule.start_cpp_function, args=(my_python_function,))
thread.start()
thread.join()  # Wait for the thread to finish

```

```
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>  // Needed for passing Python functions
#include <thread>
#include <atomic>
#include <chrono>
#include <iostream>

namespace py = pybind11;

// Function to be called from Python
void start_cpp_function(std::function<void()> py_func) {
    std::atomic<bool> finished(false);

    // Start the Python function in a separate thread
    std::thread py_thread([&]() {
        py_func();  // Call the Python function
        finished = true;  // Mark it as finished
    });

    // Monitor progress every 100ms
    while (!finished) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        std::cout << "Checking if Python function is done...\n";
    }

    py_thread.join();  // Ensure the Python thread finishes
    std::cout << "Python function has completed! Exiting C++ function.\n";
}

// Bind the function to Python using Pybind11
PYBIND11_MODULE(mymodule, m) {
    m.def("start_cpp_function", &start_cpp_function, "Start a Python function in a separate thread and monitor it.");
}

```
expected:
```
Checking if Python function is done...
Checking if Python function is done...
Checking if Python function is done...
Python function started...
Checking if Python function is done...
Python function finished.
Python function has completed! Exiting C++ function.

```

-----------------  
Boilerplate example of a thread function. Note the double wrapping with the destructor. (that ~ notation)
```
#include <iostream>
#include <thread>

class Worker {
private:
    std::thread workerThread;

    void run() {
        for (int i = 0; i < 5; ++i) {
            std::cout << "Worker thread running: " << i << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }

public:
    Worker() {
        // Assign the thread to a member variable and start it
        workerThread = std::thread(&Worker::run, this);
    }

    ~Worker() {
        if (workerThread.joinable()) {
            workerThread.join();  // Ensure thread is joined before destruction
        }
    }
};

int main() {
    Worker w;  // Thread starts automatically in constructor
    std::this_thread::sleep_for(std::chrono::seconds(3));  // Main thread waits
    std::cout << "Main thread exiting\n";
    return 0;  // Worker destructor ensures thread cleanup
```

### Relevant vscode extentions:  
- clangd
- C/C++
- C/C++ Themes
- C/C++ extension Pack
- CMake
- CMake IntelliSense
- CMake Tools



### TODO:
- dummy implementation of bt.
- write bt_tick into skeleton, make work for only a single skeleton. start with only simple printouts.
- integrate actual behaviors. Maybe move to static spot.
- take it from there. (probably work the three threads draw, tick, and action into execution)
