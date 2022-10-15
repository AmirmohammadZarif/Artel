#pragma once
#include <iostream>
#include "imgui.h"

#include "Log.h"
struct Log
{
    ImGuiTextBuffer     Buf;
    ImGuiTextFilter     Filter;
    ImVector<int>       LineOffsets; // Index to lines offset. We maintain this with AddLog() calls.
    bool                AutoScroll;  // Keep scrolling if already at the bottom.

    Log();

    void Clear();

    void AddLog(const char* fmt, ...);

    void Draw(const char* title, bool* p_open);
};
