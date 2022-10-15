#pragma once
#include <string>
#include <algorithm>
#include <sstream>
#include <utility>
#include <cstring>

class File
{
public:
	std::string windows_to_unix_file_path(std::string file_path, bool is_wsl = true);

	std::string unix_to_windows_file_path(std::string file_path, bool is_wsl = true);

	std::string windows_path_to_host_operating_system_path(std::string file_path, bool is_wsl = true);
};

