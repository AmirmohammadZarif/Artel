# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.23.2)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(sdl-populate NONE)


# Pass through things we've already detected in the main project to avoid
# paying the cost of redetecting them again in ExternalProject_Add()
set(GIT_EXECUTABLE [==[/usr/bin/git]==])
set(GIT_VERSION_STRING [==[2.30.1 (Apple Git-130)]==])
set_property(GLOBAL PROPERTY _CMAKE_FindGit_GIT_EXECUTABLE_VERSION
  [==[/usr/bin/git;2.30.1 (Apple Git-130)]==]
)


include(ExternalProject)
ExternalProject_Add(sdl-populate
                     "UPDATE_DISCONNECTED" "False" "GIT_REPOSITORY" "https://github.com/libsdl-org/SDL.git" "GIT_TAG" "1.2.15"
                    SOURCE_DIR          "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-src"
                    BINARY_DIR          "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
                    USES_TERMINAL_PATCH     YES
)


