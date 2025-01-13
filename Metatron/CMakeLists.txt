cmake_minimum_required(VERSION 3.10)

project(Metatron)

set(CMAKE_CXX_STANDARD 14)

# Specify the source files for the C++ debugger
set(SOURCE_FILES
    src/debug/cpp_debugger.cpp
)

# Add the executable for the C++ debugger
add_executable(cpp_debugger ${SOURCE_FILES})

# Include directories if needed
# include_directories(include)

# Link any required libraries
# target_link_libraries(cpp_debugger <required_libraries>)