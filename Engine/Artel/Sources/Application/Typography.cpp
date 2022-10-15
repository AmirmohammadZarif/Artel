#include "Typography.h"

void Typography::heading(char* text,int size)
{
	ImGuiIO& io = ImGui::GetIO();
	auto boldFont = io.Fonts->Fonts[size];
	ImGui::PushFont(boldFont);
	ImGui::Text(text);
	ImGui::PopFont();
}
