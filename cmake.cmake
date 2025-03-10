cmake_minimum_required(VERSION 3.20)

# Project Name and Version
project(HarmonyCompiler VERSION 1.0 LANGUAGES C CXX)

# Set C++ Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

# Detect Platform and Apply Platform-Specific Flags
if(WIN32)
    add_definitions(-DPLATFORM_WINDOWS)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /D_WIN32 /MP")  # Multi-threaded compilation on MSVC
elseif(APPLE)
    add_definitions(-DPLATFORM_MAC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D__APPLE__ -pthread")
elseif(UNIX)
    add_definitions(-DPLATFORM_LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D__linux__ -pthread")
endif()

# Output Directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Include Directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# Source Files
file(GLOB_RECURSE SRC_FILES src/*.cpp src/**/*.cpp)
file(GLOB_RECURSE HEADER_FILES include/*.h include/**/*.h)

# Compiler Options (Custom)
option(STATIC_LINK "Build with static linking" OFF)

if(STATIC_LINK)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++ -static-libgcc")
endif()

# Executable Target
add_executable(HarmonyCompiler ${SRC_FILES} ${HEADER_FILES})

# Dependencies (YAML, JSON, LLVM)
find_package(PkgConfig REQUIRED)
find_package(LLVM REQUIRED CONFIG)

pkg_check_modules(YAML_CPP REQUIRED yaml-cpp)
pkg_check_modules(JSONCPP REQUIRED jsoncpp)

# Link and Include Dependencies
target_include_directories(HarmonyCompiler PRIVATE ${YAML_CPP_INCLUDE_DIRS} ${JSONCPP_INCLUDE_DIRS} ${LLVM_INCLUDE_DIRS})
target_link_libraries(HarmonyCompiler PRIVATE ${YAML_CPP_LIBRARIES} ${JSONCPP_LIBRARIES} ${LLVM_LIBRARIES})

# Debugging Options
if(CMAKE_BUILD_TYPE MATCHES Debug)
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -DDEBUG")
endif()

# Optimization Flags for Release Builds
if(CMAKE_BUILD_TYPE MATCHES Release)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -march=native -flto")
endif()

# Testing Configuration
enable_testing()
add_subdirectory(tests)

# Install Targets (Binary + Libraries)
install(TARGETS HarmonyCompiler RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
install(FILES ${HEADER_FILES} DESTINATION include)

# Package Configuration
set(CPACK_PACKAGE_NAME "HarmonyCompiler")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION "Harmony Compiler for high-performance code execution")
set(CPACK_PACKAGE_CONTACT "support@harmonycode.org")

# Generate Installer
include(CPack)
