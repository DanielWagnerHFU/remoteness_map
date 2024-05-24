# CMakeList.txt : CMake project for euclidean_distance_transform_app, include source and define
# project specific logic here.
#

# Add source to this project's executable.
add_executable (euclidean_distance_transform_app "euclidean_distance_transform_app.cpp" "euclidean_distance_transform_app.h"    )

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET euclidean_distance_transform_app PROPERTY CXX_STANDARD 20)
endif()

# TODO: Add tests and install targets if needed.
