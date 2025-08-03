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
- [ ] High-level: Think about how tassk sequencing should work. If seeds are picked up, but no plant spot is available, how long should you hold on? What if a seed is dropped? Should it get picked up again immediately?
- [ ] steal from stardew how he did the diggable logic
    - [ ] Answer: layers & good tilemaps. PLus some entities that get spawned if you need "tile entities"
- camera logic
    - move camera position
    - correct mouse pos in a global-to-local function
    - figure out a good standardized way of interacing there.
    - Godot does this by:
        - giving vector2 a global_position function. Requires it knowing its canvasitem. THis is worldspace gobal, though.
- [ ] Only allow casting of seed spell at summong circle?
- [ ] allow skeleton summoning at graves


bt.py
- xml
- ports
- RemoteActionNode (starts thread. Perhaps puts stuff on ports and/or takes return value for success)

## Camera notes:
- Clear Code's solution is to have a camera group. Feels appropriate and pg-style, but he's specifically solving ysort issues (I will have to deal witht hese too, at some point, so it might be good anyway)
- correction: he also does camera mouse movement.
- does not, however, do a get_global_mouse_pos or whatever.

Ok, so after some thinking and video watching, I think I need some object (group?) that is the "primary camera".
Or maybe just a camera object that's assigned to whatever surface is my screen (screen is a singleton in button, but I am getting convinced that this is a bad idea).
> Is the main screen accessible in some way??
What I _want_ is a globally accesible function that allows me to get_global_mouse_pos. Godot has it as a function all Node2Ds have. It goes through the CanvasLayer it belongs to. Perhaps I can do a similar thing through the groups it belongs to??
Do I want to include layers into this camera object? How about zsorting?
And multitile objects?

## Python btree notes

possible solutions:
- player queues up a list of possible tasks (when they get "popped", how do we make sure a new scan of the environment does not immediately pick them back up again?)
- global_bb keeps track of claimed objects
- object itself keeps track of claimed status, times out after some amount of time not being refreshed
- never cancel actions? Failure is not a option!
- ask all siblings: are you going there?
- use some signal setup? Signall all who are capable of picking up?
- message queue based on objects in range, where skeletons get queue items of types they are interested in. (for whatever branch the BT is in)
    - Time out objects when adding to queue. Periodically scan for objects in range, subtracting objects in timeout list. Re-add objects to queue 
    - Alternatively, queue can be a set. Unordered, though.
    - complicating factor is that the queue will have to be recreated on player movement.
- claim action + unclaim action will have to be implemented neatly
	- if any fail: unclaimNode
	- see demo xml in claim_behavior.xml
  
Book (AI for games pg. ~568) says you will want decision making to "trickle down", higher levels do higher decision making.  
Can I make this some kind of FSM thing? Or should I assign tasks, with skeletons accepting or rejecting the job?  
Perhaps skeletons can signal to player when they're busy or idle, and they get assigned tasks through some message?  
It would be the coordinator AI's responsibility to (temporarily?) blacklist items, or mark them as "handled", until a skeleton says it's handled or rejected.

I settled on what I remembered from discussions with triplefox and Jim Stormdancer; Claim and reclaim. Have object time out claiming. This is SO much easier than it was in godot.

## What I learned from Stardew Valley:
Objects are constructed in several layers:
- AlwaysFront
- Front
- Paths
- Buildings
- Back

Each layer can have different "sublayers". Sublayers are drawn on top of each other.

- Ground is on back layer.
- Tiles that can be turned into soil are tagged as Diggable=True
- Grass, weeds, and other interactibles are placed on Paths layer (makes sense since grass and rocks destroy placed paths)
- multitile objects, like trees, and more customized object like grass (unlike weeds; I htink because you can walk "through them", and that requires some custom behavior?), are placed on Paths layer, but they have placeholder tiles in Tiled, and are replaced with (probably) object instances at runtime. I am assuming these are classes with a little bit more logic to them (tree hp, for example).
- Tiles can have custom tags like Diggable, and Type (although TYpe seems somewhatt inconsistent, and perhaps not used very consistently??)
- front and AlwaysFront are mostly used for environmental objects.
- Buildings is used for things like river edges, cliffs, and actual buildings (outside the farm; In the farm the buildings are actually spawned at runtime. Probably still into a layer, Though.)
- Buildins is also for the "footprint" of buildings, and usually denotes impassability.
- Trees tend to be grouped in Buildings, Front, and AlwaysFront pieces. I believe this is subdivided using PaintMasks.


Loading from pytmx:
```
import pygame as pg
from pytmx.util_pygame import load_pygame

pg.init()


pg.display.set_mode((1280, 960))
pg.Surface((640, 480))

txmdata=load_pygame("art/tmx/field.tmx")

# print(dir(my_tmx.tilesets[0]))
print(txmdata.tile_properties) # all tile properties
print(txmdata.get_tile_properties(14,8,1)) # get an indivitual tiles' properties, if any.
```


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
- [Warning! pygame needs to be run in the main loop, and is apparently not thread-safe. This is going to lead to problems, isn't it...?](https://stackoverflow.com/questions/2970612/pygame-in-a-thread)
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


