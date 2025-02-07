# pygame_tst

## Cheat sheet:
```
# Clone:
git clone --recurse-submodules git@github.com:yurivwarmerdam/simple_bt.git
# venv because miniconda cannot be used since its installation of sqlite3 conflicts witht he requirements of behaviortee.cpp
source venv/bin/activate
```

## Some notes:
- [pytmx](https://pytmx.readthedocs.io/en/latest/). Allows loading of tilemaps into pygame. [code snippet at this video timestamp](https://youtu.be/N6xqCwblyiw?t=4793)
- [pydew valley](https://www.youtube.com/llkwatch?v=T4IX36sP_0c) Steal this liberally

## BehaviorTree.cpp install notes:
- [behaviorTrees.cpp website](https://www.behaviortree.dev/)  
- [BehaviorTree.cpp github repo](https://github.com/BehaviorTree/BehaviorTree.CPP?tab=readme-ov-file)  

all installs have been done from source.  

Required backround apps:
```
sudo apt install libczmq-dev libsqlite3-dev sqlite pybind11-dev
```
### Links:

[The Intian guy tutorial](https://www.youtube.com/watch?v=4PUiDmD5dkg)  

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