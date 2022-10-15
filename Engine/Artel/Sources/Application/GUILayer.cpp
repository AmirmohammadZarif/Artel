#include "GUILayer.h"

// Data
static ID3D11Device* g_pd3dDevice = NULL;
static ID3D11DeviceContext* g_pd3dDeviceContext = NULL;
static IDXGISwapChain* g_pSwapChain = NULL;
static ID3D11RenderTargetView* g_mainRenderTargetView = NULL;
Image img = Image(g_pd3dDevice, g_pd3dDeviceContext, g_pSwapChain, g_mainRenderTargetView);
Typography tg;

// Forward declarations of helper functions
bool CreateDeviceD3D(HWND hWnd);
void CleanupDeviceD3D();
void CreateRenderTarget();
void CleanupRenderTarget();
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

void GUILayer::SetupWindows() {
    show_connection_window = true;
    show_studio_window = true;
    show_console_window = true;
    show_style_selector_window = false;
    show_properties_window = true;
    show_debug_window = true;
    show_logger_window = true;
    canvas_scale = 1;
    m_selected_image_file_path = "";
}

int GUILayer::Begin() {
    // Create application window
    ImGui_ImplWin32_EnableDpiAwareness();
    WNDCLASSEXW wc = { sizeof(wc), CS_CLASSDC, WndProc, 0L,   0L,       GetModuleHandle(NULL),
                      NULL,       NULL,       NULL,    NULL, L"Artel", NULL };
    ::RegisterClassExW(&wc);
    HWND hwnd = ::CreateWindowW(wc.lpszClassName, L"Artel Studio", WS_OVERLAPPEDWINDOW, 0, 0, 2560,
        1500, NULL, NULL, wc.hInstance, NULL);

    // Initialize Direct3D
    if (!CreateDeviceD3D(hwnd)) {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;
    }

    // Show the window
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);

    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    (void)io;
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // Enable Keyboard Controls
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // Enable Gamepad Controls
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;      // Enable Docking
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;  // Enable Multi-Viewport / Platform Windows

    // Setup styles
    Styles styles;
    ImGui::StyleColorsDark();

    styles.SetupStyleDarker();
    styles.SetupStyleDark();

    // Setup Platform/Renderer backends
    ImGui_ImplWin32_Init(hwnd);
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    // Load Fonts
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\segoeui.ttf", 18.0f);
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\segoeuib.ttf", 20.0f);
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\seguisb.ttf", 20.0f);
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\seguisb.ttf", 16.0f);
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\consola.ttf", 18.0f);
    io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\consolab.ttf", 18.0f);

    // Our state
    bool show_demo_window = true;
    bool show_another_window = false;
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
    img = Image(g_pd3dDevice, g_pd3dDeviceContext, g_pSwapChain, g_mainRenderTargetView);

    // Main loop
    bool done = false;
    SetupWindows();

    while (!done) {
        MSG msg;
        while (::PeekMessage(&msg, NULL, 0U, 0U, PM_REMOVE)) {
            ::TranslateMessage(&msg);
            ::DispatchMessage(&msg);
            if (msg.message == WM_QUIT) done = true;
        }
        if (done) break;

        // Start the Dear ImGui frame
        ImGui_ImplDX11_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();

        //--------------------------------------------------------
        //[Main Event]
        //-------------------------------------------------------

        ImGui::DockSpaceOverViewport(ImGui::GetMainViewport());
        MenuBar();

        if (show_connection_window) ConnectionWindow();

        if (show_console_window) Console();

        if (show_studio_window) Studio();

        if (show_style_selector_window) ShowStyleSelector("Style");

        if (show_properties_window) Properties();

        if (show_demo_window) ImGui::ShowDemoWindow(&show_demo_window);
        
        if (show_debug_window) Debug();

        if (show_logger_window) Logger(&show_logger_window);

        // Rendering
        ImGui::Render();
        const float clear_color_with_alpha[4] = { clear_color.x * clear_color.w,
                                                 clear_color.y * clear_color.w,
                                                 clear_color.z * clear_color.w, clear_color.w };
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, NULL);
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // Update and Render additional Platform Windows
        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
        }

        g_pSwapChain->Present(1, 0);
    }

    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();

    CleanupDeviceD3D();
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
    return 0;
}

/*----------------------------------------------
        [SECTION] Connection Window
----------------------------------------------*/
void GUILayer::ConnectionWindow() {
    ImGuiWindowFlags window_flags = ImGuiWindowFlags_NoCollapse;

    ImGui::Begin("Conncetion", &show_connection_window, window_flags);
       
    const char* ports[] = { "COM1", "COM2", "COM3", "COM4", "COM5" };
    static int port = 0;

    tg.heading("Connection", 2);
    ImGui::SetNextItemWidth(400);
    ImGui::Combo("Port", &port, ports, IM_ARRAYSIZE(ports));

    ImGui::SameLine();

    const char* baudrates[] = { "9600", "115200" };
    static int baudrate = 0;
    ImGui::SetNextItemWidth(300);
    ImGui::Combo("Baudrate", &baudrate, baudrates, IM_ARRAYSIZE(baudrates));

    ImGui::SameLine();
    if (ImGui::Button("Connect")) {
        connection = new SerialPort(ports[port]);
        if (connection->isConnected()) {
            ImGui::Text("Connected");
        }
    }

    ImGui::End();
}

/*----------------------------------------------
        [SECTION] Console
----------------------------------------------*/
void GUILayer::Console() {
    ImGui::Begin("Console");
    ImGui::End();
}

/*----------------------------------------------
        [SECTION] Properties
----------------------------------------------*/
void GUILayer::Properties() {
    ImGuiTreeNodeFlags heading_flags = ImGuiTreeNodeFlags_DefaultOpen;

    ImGui::Begin("Properties", &show_properties_window);
    if (ImGui::CollapsingHeader("Input", heading_flags))
    {
        int vec4i[4] = { m_selected_image_width, m_selected_image_height, m_selected_image_width, m_selected_image_height };
        
        tg.heading("Image Info", 2);
        ImGui::BeginDisabled();
        ImGui::DragInt2("###Image", vec4i, 1, 0, 6000, "%d px");
        ImGui::EndDisabled();

        input_size.x = vec4i[0];
        input_size.y = vec4i[1];

    }
    if (ImGui::CollapsingHeader("Sheet", heading_flags))
    {
        int vec4i[4] = { 12, 12, 12, 12 };
        int vec4i_tiles[4] = { 25, 25, 25, 25 };

        tg.heading("Sheet Size", 2);
        ImGui::BeginDisabled();
        ImGui::DragInt2("###SheetSize", vec4i, 1, 0, 6000, "%d cells");
        ImGui::EndDisabled();


        tg.heading("Tiles", 2);
        ImGui::BeginDisabled();
        ImGui::DragInt2("###CellDimensions", vec4i_tiles, 1, 0, 6000, "%d mm");
        ImGui::EndDisabled();


    }

    if (!m_selected_image_mat.empty() && ImGui::CollapsingHeader("Output", heading_flags))
    {
   
        static int vec4i[4] = { input_size.x, input_size.y, 100, 100 };
        static int vec4i_dimension[4] = { output_dimension.x, output_dimension.y, output_dimension.x, output_dimension.y };
        
        tg.heading("Output Size", 2);
        ImGui::DragInt2("###OutputSize", vec4i, 1, 0, 6000, "%d px");
        output_size.x = vec4i[0];
        output_size.y = vec4i[1];

        tg.heading("Output Dimension", 2);
        ImGui::DragInt2("###vec4i_dimension", vec4i, 1, 0, 6000, "%d mm");
    }

    if (ImGui::Button("Process")) {
        ImageProcessing ip;
        ip.Read(m_selected_image_file_path);

        ip.Process(ip.image, cv::Size(output_size.x, output_size.y), 8);

    }
    ImGui::End();
}

/*----------------------------------------------
        [SECTION] Studio and Canvas
----------------------------------------------*/
void GUILayer::Studio() {
    ImGui::Begin("Input");
    ImGuiIO& io = ImGui::GetIO();

    // Init
    ImGui::Text("pointer = %p", m_selected_image);
    ImGui::Text("file path = %s", m_selected_image_file_path);
    ImGui::Text("size = %d x %d", m_selected_image_width, m_selected_image_height);
    //ImGui::Image((void*)m_selected_image, ImVec2(m_selected_image_width, m_selected_image_height));
    {
        ImGui::Text("%.0fx%.0f", m_selected_image_width, m_selected_image_height);
        ImVec2 pos = ImGui::GetCursorScreenPos();
        ImVec2 uv_min = ImVec2(0.0f, 0.0f);                 // Top-left
        ImVec2 uv_max = ImVec2(1.0f, 1.0f);                 // Lower-right
        ImVec4 tint_col = ImVec4(1.0f, 1.0f, 1.0f, 1.0f);   // No tint
        ImVec4 border_col = ImVec4(1.0f, 1.0f, 1.0f, 0.5f); // 50% opaque white
        ImGui::Image((void*)m_selected_image, ImVec2(m_selected_image_width, m_selected_image_height), uv_min, uv_max, tint_col, border_col);
        if (ImGui::IsItemHovered())
        {
            ImGui::BeginTooltip();
            float region_sz = 32.0f;
            float region_x = io.MousePos.x - pos.x - region_sz * 0.5f;
            float region_y = io.MousePos.y - pos.y - region_sz * 0.5f;
            float zoom = 4.0f;
            if (region_x < 0.0f) { region_x = 0.0f; }
            else if (region_x > m_selected_image_width - region_sz) { region_x = m_selected_image_width - region_sz; }
            if (region_y < 0.0f) { region_y = 0.0f; }
            else if (region_y > m_selected_image_height - region_sz) { region_y = m_selected_image_height - region_sz; }
            ImGui::Text("Min: (%.2f, %.2f)", region_x, region_y);
            ImGui::Text("Max: (%.2f, %.2f)", region_x + region_sz, region_y + region_sz);
            ImVec2 uv0 = ImVec2((region_x) / m_selected_image_width, (region_y) / m_selected_image_height);
            ImVec2 uv1 = ImVec2((region_x + region_sz) / m_selected_image_width, (region_y + region_sz) / m_selected_image_height);
            ImGui::Image((void*)m_selected_image, ImVec2(region_sz * zoom, region_sz * zoom), uv0, uv1, tint_col, border_col);
            ImGui::EndTooltip();
        }
    }
    ImGui::End();

    ImGui::Begin("Output");
    static ImVector<ImVec2> points;
    static ImVec2 scrolling(0.0f, 0.0f);
    static bool opt_enable_grid = true;
    static bool opt_enable_context_menu = true;
    static bool adding_line = false;

    ImGui::Checkbox("Enable grid", &opt_enable_grid);
    ImGui::Checkbox("Enable context menu", &opt_enable_context_menu);

    ImGui::BeginChild("canvas");
    // ImGui::InvisibleButton("Button", ImVec2(10, 10));
    // Using InvisibleButton() as a convenience 1) it will advance the layout cursor and 2) allows
    // us to use IsItemHovered()/IsItemActive()
    ImVec2 canvas_p0 = ImGui::GetCursorScreenPos();     // ImDrawList API uses screen coordinates!
    ImVec2 canvas_sz = ImGui::GetContentRegionAvail();  // Resize canvas to what's available
    if (canvas_sz.x < 50.0f) canvas_sz.x = 50.0f;
    if (canvas_sz.y < 50.0f) canvas_sz.y = 50.0f;
    ImVec2 canvas_p1 = ImVec2(canvas_p0.x + canvas_sz.x, canvas_p0.y + canvas_sz.y);

    // Draw border and background color
    ImDrawList* draw_list = ImGui::GetWindowDrawList();
    draw_list->AddRectFilled(canvas_p0, canvas_p1, IM_COL32(50, 50, 50, 255));
    draw_list->AddRect(canvas_p0, canvas_p1, IM_COL32(255, 255, 255, 255));

    // This will catch our interactions
    ImGui::InvisibleButton("canvas", canvas_sz,
        ImGuiButtonFlags_MouseButtonLeft | ImGuiButtonFlags_MouseButtonRight);
    const bool is_hovered = ImGui::IsItemHovered();  // Hovered
    const bool is_active = ImGui::IsItemActive();    // Held
    const ImVec2 origin(canvas_p0.x + scrolling.x,
        canvas_p0.y + scrolling.y);  // Lock scrolled origin
    const ImVec2 mouse_pos_in_canvas(io.MousePos.x - origin.x, io.MousePos.y - origin.y);

    // Add first and second point
    /*
    if (is_hovered && !adding_line && ImGui::IsMouseClicked(ImGuiMouseButton_Left))
    {
            points.push_back(mouse_pos_in_canvas);
            points.push_back(mouse_pos_in_canvas);
            adding_line = true;
    }
    if (adding_line)
    {
            points.back() = mouse_pos_in_canvas;
            if (!ImGui::IsMouseDown(ImGuiMouseButton_Left))
                    adding_line = false;
    }
    */
    if (is_hovered) {
    }

    // Pan (we use a zero mouse threshold when there's no context menu)
    // You may decide to make that threshold dynamic based on whether the mouse is hovering
    // something etc.
    const float mouse_threshold_for_pan = opt_enable_context_menu ? -1.0f : 0.0f;
    if (is_active && ImGui::IsMouseDragging(ImGuiMouseButton_Left, mouse_threshold_for_pan)) {
        scrolling.x += io.MouseDelta.x;
        scrolling.y += io.MouseDelta.y;
    }

    // Context menu (under default mouse threshold)
    ImVec2 drag_delta = ImGui::GetMouseDragDelta(ImGuiMouseButton_Right);
    if (opt_enable_context_menu && drag_delta.x == 0.0f && drag_delta.y == 0.0f)
        ImGui::OpenPopupOnItemClick("context", ImGuiPopupFlags_MouseButtonRight);
    if (ImGui::BeginPopup("context")) {
        if (adding_line) points.resize(points.size() - 2);
        adding_line = false;
        if (ImGui::MenuItem("Remove one", NULL, false, points.Size > 0)) {
            points.resize(points.size() - 2);
        }
        if (ImGui::MenuItem("Remove all", NULL, false, points.Size > 0)) {
            points.clear();
        }
        ImGui::EndPopup();
    }

    // Draw grid + all lines in the canvas
    int tile_side = 25;
    int tiles_gap = 2;
    for (int i = 0; i < 72; i++) {
        for (int j = 0; j < 72; j++) {
            draw_list->AddRectFilled(
                ImVec2(origin.x + tiles_gap + (i * tile_side),
                    origin.y + tiles_gap + (j * tile_side)),
                ImVec2(origin.x + ((i + 1) * tile_side), origin.y + ((j + 1) * tile_side)),
                IM_COL32(10 + i * 3, j * 2, (i + j) * 1 + 10, 255));
        }
    }

    draw_list->PushClipRect(canvas_p0, canvas_p1, true);
    if (opt_enable_grid) {
        const float GRID_STEP = 300;
        for (float x = fmodf(scrolling.x, GRID_STEP); x < canvas_sz.x; x += GRID_STEP)
            draw_list->AddLine(ImVec2(canvas_p0.x + x, canvas_p0.y),
                ImVec2(canvas_p0.x + x, canvas_p1.y), IM_COL32(0, 200, 0, 40), 4.0f);
        for (float y = fmodf(scrolling.y, GRID_STEP); y < canvas_sz.y; y += GRID_STEP)
            draw_list->AddLine(ImVec2(canvas_p0.x, canvas_p0.y + y),
                ImVec2(canvas_p1.x, canvas_p0.y + y), IM_COL32(0, 200, 0, 40), 4.0f);
    }
    ImVec2 pos = ImGui::GetCursorScreenPos();
    ImVec2 uv_min = ImVec2(0.0f, 0.0f);                  // Top-left
    ImVec2 uv_max = ImVec2(1.0f, 1.0f);                  // Lower-right
    ImVec4 tint_col = ImVec4(1.0f, 1.0f, 1.0f, 1.0f);    // No tint
    ImVec4 border_col = ImVec4(1.0f, 1.0f, 1.0f, 0.5f);  // 50% opaque white
    if (ImGui::IsItemHovered()) {
        ImGui::BeginTooltip();
        float region_sz = 32.0f;
        float region_x = io.MousePos.x - pos.x - region_sz * 0.5f;
        float region_y = io.MousePos.y - pos.y - region_sz * 0.5f;
        float zoom = 4.0f;
        if (region_x < 0.0f) {
            region_x = 0.0f;
        }
        else if (region_x > canvas_sz.x - region_sz) {
            region_x = canvas_sz.x - region_sz;
        }
        if (region_y < 0.0f) {
            region_y = 0.0f;
        }
        else if (region_y > canvas_sz.y - region_sz) {
            region_y = canvas_sz.y - region_sz;
        }
        ImGui::Text("Min: (%.2f, %.2f)", region_x, region_y);
        ImGui::Text("Max: (%.2f, %.2f)", region_x + region_sz, region_y + region_sz);
        ImVec2 uv0 = ImVec2((region_x) / canvas_sz.x, (region_y) / canvas_sz.y);
        ImVec2 uv1 =
            ImVec2((region_x + region_sz) / canvas_sz.x, (region_y + region_sz) / canvas_sz.y);
        ImGui::EndTooltip();
    }

    draw_list->PopClipRect();
    ImGui::EndChild();
    ImGui::End();
}

/*----------------------------------------------
        [SECTION] MenuBar
----------------------------------------------*/
void GUILayer::MenuBar() {
    if (ImGui::BeginMainMenuBar()) {
        if (ImGui::BeginMenu("File")) {
            if (ImGui::MenuItem("Open", "CTRL+O")) {
                nfdchar_t* outPath = NULL;
                nfdresult_t result = NFD_OpenDialog(NULL, NULL, &outPath);
                
                if (result == NFD_OKAY) {
                    File file;
                    char* filepath = outPath;
                    m_selected_image_file_path = filepath;
                    const std::filesystem::path path = outPath;
                    ImageProcessing ip;
                    ip.Read(m_selected_image_file_path);

                    free(outPath);
                    bool ret =
                        img.LoadTextureFromFile(path.string().c_str(), &m_selected_image,
                            &m_selected_image_width, &m_selected_image_height);

                    m_selected_image_mat = ip.image;

                    input_size.x = m_selected_image_width;
                    input_size.y = m_selected_image_height;

                    input_aspect_ratio = input_size.x / input_size.y;
                    output_size.x = m_selected_image_width;
                    output_size.y = m_selected_image_height;

                    IM_ASSERT(ret);

                }
                else if (result == NFD_CANCEL) {
                    puts("User pressed cancel.");
                }
                else {
                    printf("Error: %s\n", NFD_GetError());
                }
            }

            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu("Edit")) {
            if (ImGui::MenuItem("Undo", "CTRL+Z")) {
            }
            if (ImGui::MenuItem("Redo", "CTRL+Y", false, false)) {
            }  // Disabled item
            ImGui::Separator();
            if (ImGui::MenuItem("Cut", "CTRL+X")) {
            }
            if (ImGui::MenuItem("Copy", "CTRL+C")) {
            }
            if (ImGui::MenuItem("Paste", "CTRL+V")) {
            }
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu("View")) {
            if (ImGui::MenuItem("Style Selector")) {
                show_style_selector_window = !show_style_selector_window;
            }
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu("Window")) {
            if (ImGui::MenuItem("Connection")) {
                show_connection_window = !show_connection_window;
            }
            if (ImGui::MenuItem("Console")) {
                show_console_window = !show_console_window;
            }
            if (ImGui::MenuItem("Studio")) {
                show_studio_window = !show_studio_window;
            }
            if (ImGui::MenuItem("Debug")) {
                show_debug_window = !show_debug_window;
            }
            ImGui::EndMenu();
        }
        ImGui::EndMainMenuBar();
    }
}

/*----------------------------------------------
        [SECTION] Debug
----------------------------------------------*/
void GUILayer::Debug() {
    ImGui::Begin("Debug");
    ImGui::Text("Application average %.3f ms/frame (%.1f FPS)",
        1000.0f / ImGui::GetIO().Framerate, ImGui::GetIO().Framerate);
    ImGui::End();
}

/*----------------------------------------------
        [SECTION] Style Selector
----------------------------------------------*/
bool GUILayer::ShowStyleSelector(const char* label) {
    Styles styles;

    static int style_idx = -1;
    ImGui::Begin("Style Selector");
    if (ImGui::Combo(label, &style_idx, "Dark\0Light\0Classic\0ArtelDark\0ArtelDarker")) {
        switch (style_idx) {
        case 0:
            ImGui::StyleColorsDark();
            break;
        case 1:
            ImGui::StyleColorsLight();
            break;
        case 2:
            ImGui::StyleColorsClassic();
            break;
        case 3:
            styles.SetupStyleDark();

            break;
        case 4:
            styles.SetupStyleDarker();
            break;
        }
        ImGui::End();
        return true;
    }
    ImGui::End();

    return false;
}

/*----------------------------------------------
        [SECTION] Help Marker
----------------------------------------------*/
void GUILayer::HelpMarker(const char* desc) {
    ImGui::TextDisabled("(?)");
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_DelayShort)) {
        ImGui::BeginTooltip();
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

void GUILayer::Logger(bool* p_open)
{
    static Log log;

   
    ImGui::SetNextWindowSize(ImVec2(500, 400), ImGuiCond_FirstUseEver);
    ImGui::Begin("Log", p_open);
    if (ImGui::SmallButton("[Debug] Add 5 entries"))
    {
        static int counter = 0;
        const char* categories[3] = { "info", "warn", "error" };
        const char* words[] = { "Bumfuzzled", "Cattywampus", "Snickersnee", "Abibliophobia", "Absquatulate", "Nincompoop", "Pauciloquent" };
        for (int n = 0; n < 5; n++)
        {
            const char* category = categories[counter % IM_ARRAYSIZE(categories)];
            const char* word = words[counter % IM_ARRAYSIZE(words)];
            log.AddLog("[%05d] [%s] Hello, current time is %.1f, here's a word: '%s'\n",
                ImGui::GetFrameCount(), category, ImGui::GetTime(), word);
            counter++;
        }
    }
    ImGui::End();

    log.Draw("Log", p_open);
}


int GUILayer::Run() { return 0; }

int GUILayer::End() { return 0; }


bool CreateDeviceD3D(HWND hWnd) {
    // Setup swap chain
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_0,
    };
    if (D3D11CreateDeviceAndSwapChain(NULL, D3D_DRIVER_TYPE_HARDWARE, NULL, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext) != S_OK)
        return false;

    CreateRenderTarget();
    return true;
}

void CleanupDeviceD3D() {
    CleanupRenderTarget();
    if (g_pSwapChain) {
        g_pSwapChain->Release();
        g_pSwapChain = NULL;
    }
    if (g_pd3dDeviceContext) {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = NULL;
    }
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = NULL;
    }
}

void CreateRenderTarget() {
    ID3D11Texture2D* pBackBuffer;
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, NULL, &g_mainRenderTargetView);
    pBackBuffer->Release();
}

void CleanupRenderTarget() {
    if (g_mainRenderTargetView) {
        g_mainRenderTargetView->Release();
        g_mainRenderTargetView = NULL;
    }
}

#ifndef WM_DPICHANGED
#define WM_DPICHANGED 0x02E0  // From Windows SDK 8.1+ headers
#endif

// Forward declare message handler from imgui_impl_win32.cpp
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam,
    LPARAM lParam);

// Win32 message handler
// You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to
// use your inputs.
// - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application, or
// clear/overwrite your copy of the mouse data.
// - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main
// application, or clear/overwrite your copy of the keyboard data. Generally you may always pass all
// inputs to dear imgui, and hide them from your application based on those two flags.
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam)) return true;

    switch (msg) {
    case WM_SIZE:
        if (g_pd3dDevice != NULL && wParam != SIZE_MINIMIZED) {
            CleanupRenderTarget();
            g_pSwapChain->ResizeBuffers(0, (UINT)LOWORD(lParam), (UINT)HIWORD(lParam),
                DXGI_FORMAT_UNKNOWN, 0);
            CreateRenderTarget();
        }
        return 0;
    case WM_SYSCOMMAND:
        if ((wParam & 0xfff0) == SC_KEYMENU)  // Disable ALT application menu
            return 0;
        break;
    case WM_DESTROY:
        ::PostQuitMessage(0);
        return 0;
    case WM_DPICHANGED:
        if (ImGui::GetIO().ConfigFlags & ImGuiConfigFlags_DpiEnableScaleViewports) {
            // const int dpi = HIWORD(wParam);
            // printf("WM_DPICHANGED to %d (%.0f%%)\n", dpi, (float)dpi / 96.0f * 100.0f);
            const RECT* suggested_rect = (RECT*)lParam;
            ::SetWindowPos(hWnd, NULL, suggested_rect->left, suggested_rect->top,
                suggested_rect->right - suggested_rect->left,
                suggested_rect->bottom - suggested_rect->top,
                SWP_NOZORDER | SWP_NOACTIVATE);
        }
        break;
    }
    return ::DefWindowProc(hWnd, msg, wParam, lParam);
}
