# pygame_tst

## Cheat sheet:
```
# Clone:
git clone --recurse-submodules git@github.com:yurivwarmerdam/simple_bt.git
# venv because miniconda cannot be used since its installation of sqlite3 conflicts with he requirements of behaviortee.cpp
source venv/bin/activate
```

environment setup install script:
```
sudo apt install libczmq-dev libsqlite3-dev pybind11-dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



## TODO:
- [x] dummy implementation of bt.
- add tcking the btree (in skeleton; inherit, or instantiate?) to main loop, and tick on timer (~250ms).
- write bt_tick into skeleton, make work for only a single skeleton. start with only simple printouts.
- integrate actual behaviors. Maybe move to static spot.
- take it from there. (probably work the three threads draw, tick, and action into execution)
- boost stuff: https://theboostcpplibraries.com/boost.thread-management


bt.py
- xml
- ports
- RemoteActionNode (starts thread. Perhaps puts stuff on ports and/or takes return value for success)


## Python btree notes

possible solutions:
- player queues up a list of possible tasks (when they get "popped", how do we make sure a new scan of the environment does not immediately pick them back up again?)
- global_bb keeps track of claimed objects
- object itself keeps track of claimed status, times out after some amount of time not being refreshed
- never cancel actions? Failure is not a option!
- ask all siblings: are you going there?
- use some signal setup? Signall all who are capable of picking up?

- claim action + unclaim action will have to be implemented neatly
	- if any fail: unclaimNode
	- see demo xml in claim_behavior.xml
  
Book (AI for games pg. ~568) says you will want decision making to "trickle down", higher levels do higher decision making.  
Can I make this some kind of FSM thing? Or should I assign tasks, with skeletons accepting or rejecting the job?  
Perhaps skeletons can signal to player when they're busy or idle, and they get assigned tasks through some message?  
It would be the coordinator AI's responsibility to (temporarily?) blacklist items, or mark them as "handled", until a skeleton says it's handled or rejected.


## pygame
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

### Pygame Links


- The BT paper: https://arxiv.org/pdf/1709.00084  
- Indian demo P3 github: https://github.com/thehummingbird/robotics_demos/blob/main/behavior_trees/grasp_place_robot_demo/bt_demo.cpp
- [pytmx](https://pytmx.readthedocs.io/en/latest/). Allows loading of tilemaps into pygame. [code snippet at this video timestamp](https://youtu.be/N6xqCwblyiw?t=4793)
- [pydew valley](https://www.youtube.com/watch?v=T4IX36sP_0c) Steal this liberally

## Relevant vscode extentions:  
- clangd
- C/C++
- C/C++ Themes
- C/C++ extension Pack
- CMake
- CMake IntelliSense
- CMake Tools





## unsorted links:
- [Warning! pygame needs t be run in the main loop, and is apparently not thread-safe. This is going to lead to problems, isn't it...?](https://stackoverflow.com/questions/2970612/pygame-in-a-thread)
- [Some more StackOverflow discussion on "making the right choice" when doing asynchronous programming](https://stackoverflow.com/questions/27435284/multiprocessing-vs-multithreading-vs-asyncio)
- [conference talk about what coroutines are anyway, looks like it's for those who use them already, so interesting!](https://www.youtube.com/watch?v=GSiZkP7cI80)

## BehaviorTree.cpp
### install notes:
- [behaviorTrees.cpp website](https://www.behaviortree.dev/)  
- [BehaviorTree.cpp github repo](https://github.com/BehaviorTree/BehaviorTree.CPP?tab=readme-ov-file)  
all installs have been done from source.  

### BTree.cpp Links:

[The Hummingbird tutorial P2](https://www.youtube.com/watch?v=4PUiDmD5dkg)  
[The Hummingbird tutorial P3](https://www.youtube.com/watch?v=T_Q57-audMk)  

[Sample Project](https://github.com/BehaviorTree/btcpp_sample)

[Official Tutorials](https://www.behaviortree.dev/docs/category/tutorials-basic/)

- [General intro to BTrees](https://www.youtube.com/watch?v=DCZJUvTQV5Q)  
- [pytrees](https://py-trees.readthedocs.io/en/devel/introduction.html)  

### And similar cpp links:
- Currently looking at pybind11: https://www.youtube.com/watch?v=_5T70cAXDJ0  
- Corresponding gist: https://gist.github.com/safijari/f7aec85b89906b4b90a8f33039c11263  
functors: https://www.geeksforgeeks.org/functors-in-cpp/  


