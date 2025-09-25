@echo off
REM Build script for OpenXilEnv using Conan and CMake
REM Make sure MinGW, CMake, Ninja, and Conan are in your PATH

echo Building OpenXilEnv with Conan...

REM Create build directory
if not exist "build" mkdir build
cd build

REM Install dependencies and build
echo Installing dependencies with Conan...
conan install .. -pr:h=../conan_profiles/mingw14_claude -pr:b=../conan_profiles/buildtools --build=missing

echo Building project...
cmake .. -G Ninja -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
ninja

echo Build complete!
echo.
echo To run the application, make sure Qt6 DLLs are in your PATH or use:
echo windeployqt6.exe XilEnvGui.exe

pause