# OpenXilEnv

OpenXilEnv is a lightweight SiL/HiL environment. At the moment, OpenXilEnv focuses on one SiL environment.

---

## SiL

With a **S**oftware **I**n the **L**oop system, it is possible to run and test embedded software without a target platform or compiler.
XilEnv provides an environment to set up a SiL system on Windows or Linux hosts. It clearly separates its own components from the embedded software under test through a network layer. Each component can run in its own executable, providing memory protection between them.

Communication between the software under test, models, and XilEnv is done via sockets or (on Windows) Named Pipes / (on Linux) local sockets. These are used for:
- Signal transfers
- Virtual network (CAN and CAN FD) transfers

![XilEnv SiL system](OpenXilEnv_Sil.png)

**XilEnvGui** provides a configurable graphical user interface based on Qt. It includes display/change widgets, oscilloscopes, calibration tools, sliders, knobs, and other interaction elements.

**XilEnv** (CLI) has no graphical user interface and can be used for automation without user interaction.

Main features:
- Supports current GCC compilers with DWARF debug information. Visual Studio compiler is supported but without debug information.
- FMUs with FMI 2.0 interface are supported via **ExtProc_FMU2Extract(.exe)**, **ExtProc_FMU2Loader32(.exe)**, and **ExtProc_FMU2Loader64(.exe)**.
- Partial FMI 3.0 support (additional datatypes only) via **ExtProc_FMU3Extract(.exe)**, **ExtProc_FMU3Loader32(.exe)**, and **ExtProc_FMU3Loader64(.exe)**.
- Includes a small A2L parser for calibration.
- Supports XCP over Ethernet for connection to a calibration system.
- Multicore support with synchronization barriers.
- Automatable via **XilEnvRpc.dll/.so** or the built-in script interpreter.
- Supports 32- and 64-bit executables (mixed allowed). XilEnv itself must be 64-bit.
- Time simulation with fixed, configurable period and 1 ns resolution.
- Residual bus simulation for missing CAN (FD) members.
- Recording and stimulation supported via text or MDF3 files.

The DLL/shared library **XilEnvExtProc64.dll/.so** or **XilEnvExtProc32.dll/.so** provides the interface for the embedded test software or model. This DLL/shared library must be loaded dynamically. The main module **XilEnvExtProcMain.c** handles this automatically.

Interface functions are declared in **XilEnvRtProc.h**.

An example can be found in `Samples/ExternalProcesses/ExtProc_Simple`.

---

## HiL Option

To use OpenXilEnv as a HiL system, a second Linux PC is required. Currently, only SocketCAN (FD) interfaces are supported.

A defined time response of <1 ms is achievable if the RT-Preempt patch is installed.

To meet deterministic timing requirements, XilEnv is split into two parts:
- **LinuxRemoteMasterCore.so**: components with defined time response (run on Linux with RT-Preempt)
- **XilEnv executable**: non–real-time components (can run on Windows or Linux)

A direct Ethernet connection between both PCs is recommended.

If a model is required, it must be compiled for Linux and linked with **LinuxRemoteMasterCore.so**.

If no model is needed, use **LinuxRemoteMaster.out**.

The **RemoteStartServer** service should be installed and active on the second PC so that XilEnv can copy and start required executables remotely.

---

## Table of Contents

- [Build Instructions](#build-instructions)
  - [Windows](#windows)
    - [Install Dependencies](#install-dependencies-windows)
    - [Build Options](#build-options-windows)
    - [Build and Install](#build-and-install-windows)
    - [Run Example](#run-example-windows)
  - [Linux](#linux)
    - [Install Dependencies](#install-dependencies-linux)
    - [Build Options](#build-options-linux)
    - [Build and Install](#build-and-install-linux)
    - [Run Example](#run-example-linux)
- [Setting up Your Project](#setting-up-your-project)
- [Setup an External Process](#setup-an-external-process)

---

## Build Instructions

### Windows

#### Install Dependencies

- Qt 5.12.9 – 6.7.2  
- MinGW 11.2  
- Strawberry Perl  
- CMake (latest recommended)  
- Optional:  
  - [pugixml 1.11](https://pugixml.org/) (required if `-DBUILD_WITH_FMU2_SUPPORT=ON` or `-DBUILD_WITH_FMU3_SUPPORT=ON`)
  - [FMU Parser FMI 2.0 / 3.0](https://github.com/modelica/fmi-standard)

#### Build Options
```bash
-DBUILD_EXAMPLES=ON/OFF (default ON)
-DBUILD_WITH_FMU2_SUPPORT=ON/OFF (default OFF)
  -DFMI2_SOURCE_PATH=<path>
  -DPUGIXML_SOURCE_PATH=<path>
-DBUILD_WITH_FMU3_SUPPORT=ON/OFF (default OFF)
  -DFMI3_SOURCE_PATH=<path>
  -DPUGIXML_SOURCE_PATH=<path>
-DBUILD_ESMINI_EXAMPLE=ON/OFF (default OFF)
  -DESMINI_LIBRARY_PATH=<path>
-DCMAKE_BUILD_TYPE=Debug/Release (default Release)
-DCMAKE_INSTALL_PREFIX=../install_win
-DBUILD_32BIT=ON/OFF (default OFF)
```

#### Build and Install
```cmd
mkdir C:\path\to\openxilenv\build_win
cd C:\path\to\openxilenv\build_win
set PATH=[PathToQt]\bin;%PATH%
set PATH=[PathToGCC]\bin;%PATH%
set PATH=[PathToStrawberry]\perl\bin;%PATH%
set PATH=[PathToCMake]\bin;%PATH%
cmake -G "Ninja" [CMakeSourceDir] [Options]
cmake --build .
cmake --install .
```

#### (Optional) Deploy Qt DLLs
```cmd
cd C:\path\to\openxilenv\install_win
windeployqt6.exe XilEnvGui.exe
```

#### Run Example
```cmd
cd C:\path\to\openxilenv\install_win
XilEnvGui.exe -ini ..\Samples\Configurations\ElectricCarSample.ini
```

---

### Linux

#### Install Dependencies

- Qt 5.12.9 – 6.7.2  
- CMake  
- Optional: pugixml 1.11 and FMU parser (same as above)

#### Build and Install
```bash
mkdir ~/openxilenv/build_linux
cd ~/openxilenv/build_linux
cmake -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=../install_linux -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
cmake --install .
```

#### Run Example
```bash
cd ~/openxilenv/install_linux
./XilEnvGui -ini ../Samples/Configurations/ElectricCarSample.ini
```

#### Build Options
*(Same as Windows section.)*

---

## Setting up Your Project

### Setup an External Process

An external process must implement the following four functions:

```c
void reference_varis(void);
int init_test_object(void);
void cyclic_test_object(void);
void terminate_test_object(void);
```

These functions define initialization, cyclic behavior, and termination of your test object.

Example: `Samples/ExternalProcesses/ExtProc_Simple.c`

```c
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define XILENV_INTERFACE_TYPE XILENV_DLL_INTERFACE_TYPE
#include "XilEnvExtProc.h"
#include "XilEnvExtProcMain.c"

short Ramp;
double Sinus;
short Random;
double SampleTime;

volatile const short BOTTOM_LIMIT_RAMP = 0;
volatile const short UPPER_LIMIT_RAMP = 1000;
volatile const double SINUS_AMPLITUDE  = 1.0;
volatile const double SINUS_FREQUENCY = 0.2;

void reference_varis(void)
{
    REFERENCE_WORD_VAR(Ramp, "Ramp");
    REFERENCE_DOUBLE_VAR(Sinus, "Sinus");
    REFERENCE_WORD_VAR(Random, "Random");
    REFERENCE_DOUBLE_VAR(SampleTime, "XilEnv.SampleTime");
}

int init_test_object(void)
{
    return 0;
}

void cyclic_test_object(void)
{
    static double SinusTime;
    if (Ramp++ > UPPER_LIMIT_RAMP) Ramp = BOTTOM_LIMIT_RAMP;
    SinusTime += 2.0 * M_PI * SampleTime * SINUS_FREQUENCY;
    Sinus = SINUS_AMPLITUDE * sin(SinusTime);
    Random = rand();
}

void terminate_test_object(void) {}
```

Build example:
```bash
# Windows
gcc -g -I "C:\path\to\openxilenv\install_win\include" ExtProc_Simple.c -o ExtProc_Simple.exe

# Linux
gcc -g -I ~/openxilenv/install_linux/include ExtProc_Simple.c -ldl -lpthread -o ExtProc_Simple
```

Run example:
```bash
# Windows
set PATH=%PATH%;C:\path\to\openxilenv\install_win
ExtProc_Simple.exe -q2 XilEnvGui.exe -ini C:\path\to\ElectricCarSample.ini

# Linux
export PATH=$PATH:~/openxilenv/install_linux
./ExtProc_Simple -q2 XilEnvGui -ini ~/openxilenv/Samples/Configurations/ElectricCarSample.ini
```
Ensure both ExtProc_Simple and XilEnvGui are available in the same folder or included in your PATH.

## License
This project is part of the Eclipse Foundation and licensed under the [Apache License 2.0](LICENSE.txt).

## Contributing
Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.