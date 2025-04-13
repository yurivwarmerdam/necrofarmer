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

### Interrupting behavior from inside python:

According to the app that shall not be named:
```
import signal

def my_function():
    try:
        while True:
            print("Running...")
    except KeyboardInterrupt:
        print("Stopped.")

# Call interrupt_python() from C++ to stop the function

```

Perhaps I can have it 


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
- boost stuff: https://theboostcpplibraries.com/boost.thread-management


bt.py
- xml
- ports
- RemoteActionNode (starts thread. Perhaps puts stuff on ports and/or takes return value for success)


bb:
K1:v1

tr:  <- this part will only become relevant once I build the treebuilder/parser!!
K1->y1 <- should this be a copy??


nd:
y1:v1

take home here: the TREE makes a mapping from bb key to node key (and probably still refers the same underlying value; so passing the value by reference)


## Thinking baout concurrency:

# parallel stufff

## multiprocessing

from multiprocessing import Process, Queue

def put_square(number, queue):
	queue.put(number*number)



## coroutines!

```
import asyncio
import time

async def long_function():
	print("start")
	await asyncio.sleep(1) # Moment execution can be interrupted. Needs to be an awaitable thing.
	print("done")
	return


async def main():

batch=asyncio.gather(long_function(),long_function())
result_a, result_b= await batch # non-optional await the funcitons to finish

# Alternative syntax:

task_a=asyncio.create_task(long_function())
task_b=asyncio.create_task(long_function())

result_a= await task_a
result_v= await task_b

if __name__ == "__main__":
	asyncio.run(main()) # method of running asyncio (async) functions.
```


soo.... something like
```
# this stuff is absolutely wrong, but the very general thought is right.
# Probably have to use something 
def update_wrapper(self)
	await self.update_all()

def draw_wrapper()
	await self.draw_all()

def tree_wrapper()
	await 
```
Some god-awful, and confidently wrong GPT code. It has a point that the await should be there, though.  
I should combine what is below with call_soon(), call_later(), and call_at(). That should get me on a really good path. [Here are the python docs on call_() behavior (it's called Event loop?) that gets run in asyncio](https://docs.python.org/3/library/asyncio-eventloop.html).
Maybe I won't need to call this stuff directly, but just understanding it should help a TON. 
There might still be some need for queues (asyncio works witht he GIL, right?)? I hope not, but we'll see.
```
import asyncio
import time

async def draw_loop():
    while True:
        await asyncio.sleep(1 / 60)  # ~16.67ms
        print("Draw frame")

async def update_loop():
    while True:
        await asyncio.sleep(1 / 60)
        print("Game update")

async def behavior_tree_loop():
    while True:
        await asyncio.sleep(0.25)  # Trigger every ~250ms
        print("Update behavior trees")
```
paralellism


semi-sidenote:
- yield! Allows you to repeatedly call a function (called a generator, apparently). It keeps some internal state. It's like a repeatable return. Pauses after yielding, keeps going until its next yield, next time it's called. Can be called with a for loop, of using next().
Duh. This also applies to the main loop. THat can absolutely be run using yield.
-> [Reddit discussion/examples on yield](ttps://www.reddit.com/r/pygame/comments/144ihia/asynchronous_event_handling_example/?rdt=63579)
-> [yield examples brought up in the reddit thtread](https://github.com/rbaltrusch/pygame_examples/blob/master/code/async_events/main.py)

sidenote:
- learn about command patterns... (relevant when processing things in input loop/events.)



### links:
- [Warning! pygame needs t be run in the main loop, and is apparently not thread-safe. This is going to lead to problems, isn't it...?](https://stackoverflow.com/questions/2970612/pygame-in-a-thread)
- [Some more StackOverflow discussion on "makign the right choice" when doing asynchronous programming](https://stackoverflow.com/questions/27435284/multiprocessing-vs-multithreading-vs-asyncio)
- [conference talk about what coroutines are anyway, looks like it's for those who use them already, so interesting!](https://www.youtube.com/watch?v=GSiZkP7cI80)