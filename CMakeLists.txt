cmake_minimum_required(VERSION 2.8.3)
project(agribot_monitoring)

find_package(catkin REQUIRED COMPONENTS
  sensor_msgs
  rospy
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch key
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ".svn" EXCLUDE
)

catkin_install_python(PROGRAMS
   scripts/monitoring_node.py
   scripts/monitor_class.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
