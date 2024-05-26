include_directories(${OpenCV_INCLUDE_DIRS})
add_executable (app   "App.cpp")
target_link_libraries(app PUBLIC ${OpenCV_LIBS})
target_link_libraries(app PRIVATE core)
target_include_directories(app
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../core/include
)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET app PROPERTY CXX_STANDARD 20)
endif()
