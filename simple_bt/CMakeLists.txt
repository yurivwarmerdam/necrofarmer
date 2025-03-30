### Required ###
cmake_minimum_required(VERSION 3.16.3)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

### project ###
project(simple_bt)
SET(SRC ${CMAKE_SOURCE_DIR}/src CACHE PATH "project source")
SET(BIN ${CMAKE_SOURCE_DIR}/bin "project runnable binaries")

### third-party libraries ###

SET(BTREEC_INC ${SRC}/BehaviorTree.CPP/include/behaviortree_cpp "include dir containing all header files from external source.")
SET(BTREEC_LIB ${BIn}/BehaviorTree.CPP "location of .so from external project build dir")

find_package(PythonLibs 3.12 REQUIRED)
find_package(Boost COMPONENTS REQUIRED python)
find_package(pybind11 REQUIRED)
# find_package(Boost 1.45.0 COMPONENTS thread) 
find_package(Boost COMPONENTS thread) 

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")

### Iclude and link stuff ###


INCLUDE_DIRECTORIES(
    ${BTREEC_INC}
    ${CMAKE_SOURCE_DIR}/src
    ${Boost_INCLUDE_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
)

LINK_DIRECTORIES(
    ${BTREEC_LIB}
)
ADD_LIBRARY(simple_lib SHARED
    ${SRC}/simple_bt.cpp
)

ADD_EXECUTABLE(simple_run
    ${SRC}/simple_run.cpp
)
TARGET_LINK_LIBRARIES(simple_lib
    behaviortree_cpp
    ${Boost_LIBRARIES}
    ${PYTHON_LIBRARIES}
    ${Boost_LIBRARIES}
)
TARGET_LINK_LIBRARIES(simple_run
    simple_lib
    behaviortree_cpp
    ${Boost_LIBRARIES}
    ${PYTHON_LIBRARIES}
    ${Boost_LIBRARIES}
)

# target_compile_options(simple_lib PRIVATE -fvisibility=hidden)
# target_compile_options(simple_run PUBLIC -fvisibility=hidden)


pybind11_add_module(simple_run_bind src/simple_bt.cpp)

TARGET_LINK_LIBRARIES(simple_run_bind PUBLIC
    behaviortree_cpp
    ${PYTHON_LIBRARIES}
)
# You are doing something wrong with teh target link libraries. NO idea what yet.
# You are also facing the same issue as this guy:
# https://stackoverflow.com/questions/69525592/undefined-symbol-error-when-linking-pybind11-with-a-dynamic-library-that-calls-a/69571412#69571412
# https://github.com/pybind/pybind11/discussions/3356
