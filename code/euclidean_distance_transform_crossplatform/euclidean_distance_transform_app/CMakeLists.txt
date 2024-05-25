include_directories(${OpenCV_INCLUDE_DIRS})
add_executable (euclidean_distance_transform_app "euclidean_distance_transform_app.cpp" "euclidean_distance_transform_app.h")
target_link_libraries(euclidean_distance_transform_app PUBLIC ${OpenCV_LIBS})

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET euclidean_distance_transform_app PROPERTY CXX_STANDARD 20)
endif()
