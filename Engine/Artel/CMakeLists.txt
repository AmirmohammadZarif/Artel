#
# CMake build system for Dear ImGui
# =================================
#
# Build instructions:
# 1. Install latest CMake
#   * Windows: https://cmake.org/download/ (Tick checkbox to place cmake in system PATH)
#   * Linux: from your favorite package manager
#   * MacOS: brew install cmake
# 2. Open command prompt in directory containing "imgui" and "imgui_dev" folders
#   * Windows: open Visual Studio tools command prompt or specify -G "Generator Name" (quotes are important).
#   * Other platforms: Specifying generator name is optional.
# 3. Create a build directory and configure build
#    git clone https://github.com/ocornut/imgui.git
#    mkdir cmake-build
#    cd cmake-build
#    cmake <optional build parameters> ../imgui
# 4. Build
#   * Windows (Visual Studio generators): Open generated imgui_dev.sln
#   * All platforms: cmake --build .
#
# Example of using Dear ImGui in your CMake project:
#
#   # Set various library options:
#   set(IMGUI_SDL_TARGET sdl CACHE STRING "" FORCE)
#   # Include Dear ImGui into build.
#   add_subdirectory(path/to/imgui)
#   <..>
#   # Link Dear ImGui to your application:
#   #  imgui - a main library target
#   #  imgui-sdl - a platform backend target
#   #  imgui-dx11 - a graphics backend target
#   target_link_libraries(YourApplication PUBLIC imgui imgui-sdl imgui-dx11)
#
# A list of defined targets:
#   imgui-sdl: platform backend for Windows/Linux/MacOS/etc using SDL2.
#   imgui-glfw: platform backend for Windows/Linux/MacOS/etc using GLFW.
#   imgui-osx: platform backend for MacOS.
#   imgui-win32: platform backend for Windows.
#   imgui-glut: platform backend for Windows/Linux/MacOS using glut/freeglut with OpenGL.
#   imgui-metal: graphics backend for MacOS using Metal graphics API.
#   imgui-opengl3: graphics backend for Windows/Linux/MacOS/etc using OpenGL3 graphics API.
#   imgui-opengl2: graphics backend for Windows/Linux/MacOS/etc using OpenGL2 graphics API.
#   imgui-vulkan: graphics backend for Windows/Linux/MacOS/etc using Vulkan graphics API.
#   imgui-dx9: graphics backend for Windows using DirectX 9 graphics API.
#   imgui-dx10: graphics backend for Windows using DirectX 10 graphics API.
#   imgui-dx11: graphics backend for Windows using DirectX 11 graphics API.
#   imgui-dx12: graphics backend for Windows using DirectX 12 graphics API.
#   imgui-sdlrenderer: graphics backend for platforms supported by SDL.
#
cmake_minimum_required (VERSION 3.13)
project (artel)
# Set various library options:
set(IMGUI_SDL_TARGET sdl CACHE STRING "" FORCE)
# Include Dear ImGui into build.
add_subdirectory(libs/imgui)

target_link_libraries(artel PUBLIC imgui imgui-sdl imgui-opengl3)