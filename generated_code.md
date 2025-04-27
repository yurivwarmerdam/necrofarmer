
## Gross generated code to peek at:
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

### multiprocessing

from multiprocessing import Process, Queue

def put_square(number, queue):
	queue.put(number*number)



### coroutines!
now a better, actually working implementation than this slop below. Look in skeleton.py>RandomWait for details.

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

-> [wonderful example of asyncio with pygame](https://blubbervision.neocities.org/asyncio)  
-> [part II](https://blubberquark.tumblr.com/post/177942351040/  asyncio-for-the-working-pygame-programmer-part)

## How to get a solid tick rate:

```
async def fixed_rate_task():
    while True:
        start = asyncio.get_event_loop().time()
        # Do the important work
        await do_important_work()
        elapsed = asyncio.get_event_loop().time() - start
        await asyncio.sleep(max(0, 1/60 - elapsed))  # maintain ~60Hz

async def flexible_task():
    while True:
        # Do the less important work
        await do_flexible_work()
        await asyncio.sleep(1)  # runs once every second


async def main():
    asyncio.create_task(fixed_rate_task())
    asyncio.create_task(flexible_task())
    await asyncio.Event().wait()  # keep the program running

asyncio.run(main())

```
