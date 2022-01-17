cmake_minimum_required(VERSION 3.0.2)
project(ros_cv_pkg)

add_compile_options(-std=c++17)

find_package(catkin_simple REQUIRED)
find_package(OpenCV REQUIRED)
catkin_simple(ALL_DEPS_REQUIRED)
find_package(catkin REQUIRED COMPONENTS)

catkin_package()

catkin_install_python(
  PROGRAMS src/ros2cv.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


