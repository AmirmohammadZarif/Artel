# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-src"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-build"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix/tmp"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix/src/sdl-populate-stamp"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix/src"
  "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix/src/sdl-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/amirmohammad/Documents/Projects/Artman/Delta Robot/Software/Client/CPP Version/Artel/build/_deps/sdl-subbuild/sdl-populate-prefix/src/sdl-populate-stamp/${subDir}")
endforeach()
