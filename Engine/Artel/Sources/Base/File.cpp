#include "File.h"
static const char* const WSL_FILE_PATH_HEADER = "/mnt";
static const char WINDOWS_FILE_PATH_SEPARATOR = '\\';
static const char UNIX_FILE_PATH_SEPARATOR = '/';

std::string File::windows_to_unix_file_path(std::string file_path, bool is_wsl) {
    // Replace the slashes
    std::replace(file_path.begin(), file_path.end(), WINDOWS_FILE_PATH_SEPARATOR, UNIX_FILE_PATH_SEPARATOR);

    // Convert the drive letter to lowercase
    std::transform(file_path.begin(), file_path.begin() + 1, file_path.begin(),
        [](unsigned char character) {
        return std::tolower(character);
    });

    // Remove the colon
    const auto drive_letter = file_path.substr(0, 1);
    const auto remaining_path = file_path.substr(2, file_path.size() - 2);
    file_path = drive_letter + remaining_path;

    std::stringstream stringstream;

    if (is_wsl) {
        stringstream << WSL_FILE_PATH_HEADER;
    }

    stringstream << "/";
    stringstream << file_path;

    return stringstream.str();
}

std::string File::unix_to_windows_file_path(std::string file_path, bool is_wsl) {
    if (is_wsl) {
        file_path = file_path.erase(0, strlen(WSL_FILE_PATH_HEADER));
    }

    // Delete the leading forward slash
    file_path.erase(0, 1);

    // Convert the drive letter to uppercase
    std::transform(file_path.begin(), file_path.begin() + 1, file_path.begin(),
        [](unsigned char character) {
        return std::toupper(character);
    });

    // Replace the slashes
    std::replace(file_path.begin(), file_path.end(), UNIX_FILE_PATH_SEPARATOR,
        WINDOWS_FILE_PATH_SEPARATOR);

    std::stringstream stringstream;
    stringstream << file_path.at(0);
    stringstream << ":";
    stringstream << file_path.substr(1, file_path.size() - 1);

    return stringstream.str();
}

std::string File::windows_path_to_host_operating_system_path(std::string file_path, bool is_wsl) {
#ifdef _WIN32
    return file_path;

#else
    return windows_to_unix_file_path(std::move(file_path), is_wsl);

#endif
}