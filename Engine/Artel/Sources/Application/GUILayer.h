#pragma once
#include "../Artel.h"
#define IM_ARRAYSIZE(_ARR)          ((int)(sizeof(_ARR) / sizeof(*(_ARR))))

class GUILayer
{
public:
	
	// Panels configuration
	bool show_connection_window;
	bool show_console_window;
	bool show_studio_window;
	bool show_style_selector_window;
	bool show_properties_window;
	bool show_debug_window;
	bool show_logger_window;

	SerialPort* connection;
	const char* portName = "\\\\.\\COM5";

	void SetupStyleDarker();
	void ConnectionWindow();
	void Console();
	void Properties();
	void Studio();
	void HelpMarker(const char* desc);
	void Logger(bool* p_open);
	void Debug();
	bool ShowStyleSelector(const char* label);
	void MenuBar();
	void SetupStyle();
	void SetupWindows();
	int Begin();
	int Run();
	int End();
private:
	ID3D11ShaderResourceView* m_selected_image;
	Mat m_selected_image_mat;
	int m_selected_image_width;
	int m_selected_image_height;
	std::string m_selected_image_file_path;
	float canvas_scale;
	float input_aspect_ratio;
	ImVec2 input_size;
	ImVec2 sheet_size;
	ImVec2 output_size;
	ImVec2 output_dimension;
};

