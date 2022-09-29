#ifndef APPLICATION_H
#define APPLICATION_H

#include "imgui.h"
#include "Robot.h"
#include "imgui_impl_sdl.h"
#include "imgui_impl_opengl3.h"
#include <stdio.h>
#include <math.h>
#include "Jogging.h"
#include <SDL.h>
#include "../libs/serial/include/serial/serial.h"
#if defined(IMGUI_IMPL_OPENGL_ES2)
#include <SDL_opengles2.h>
#else
#include <SDL_opengl.h>
#endif

namespace Artel
{
    class Application
    {
    public:
        void SetupStyle();
        int Run();
        int main();
    };
}

#endif // !APPLICATION_H