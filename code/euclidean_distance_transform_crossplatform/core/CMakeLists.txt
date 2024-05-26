include_directories(${OpenCV_INCLUDE_DIRS})
add_library(core STATIC "src/CV2EuclideanDistanceTransformStrategy.cpp" "src/DistanceTransformContext.cpp" )
target_link_libraries(core PUBLIC ${OpenCV_LIBS})
target_include_directories(core
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET core PROPERTY CXX_STANDARD 20)
endif()


