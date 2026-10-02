cmake_minimum_required(VERSION 3.28)
project(smiley LANGUAGES CXX)

option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

include(FetchContent)
FetchContent_Declare(SFML
        GIT_REPOSITORY https://github.com/SFML/SFML.git
        GIT_TAG 3.0.2
        GIT_SHALLOW ON
        EXCLUDE_FROM_ALL
        SYSTEM)
FetchContent_MakeAvailable(SFML)

add_executable(smiley main.cpp)
target_compile_features(smiley PRIVATE cxx_std_17)
target_link_libraries(smiley PRIVATE SFML::Graphics)
