from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy
import os


class OpenXilEnvConan(ConanFile):
    name = "openxilenv"
    version = "10.0"
    package_type = "application"

    # Optional metadata
    license = "Eclipse Public License 2.0"
    author = "Eclipse OpenXilEnv"
    url = "https://github.com/eclipse-openxilenv/openxilenv"
    description = "OpenXilEnv is a lightweight SIL/HIL environment"
    topics = ("simulation", "automotive", "testing", "sil", "hil")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "Src/*", "Samples/*", "Tools/*", "Userguide/*"

    # Options that can be passed to cmake
    options = {
        "build_examples": [True, False],
        "build_with_fmu2_support": [True, False],
        "build_with_fmu3_support": [True, False],
        "build_esmini_example": [True, False],
        "build_with_j1939_support": [True, False],
        "build_with_gateway_virtual_can": [True, False],
        "build_with_pdb_reader_dll_interface": [True, False],
        "build_32bit": [True, False],
    }

    default_options = {
        "build_examples": True,
        "build_with_fmu2_support": False,
        "build_with_fmu3_support": False,
        "build_esmini_example": False,
        "build_with_j1939_support": False,
        "build_with_gateway_virtual_can": False,
        "build_with_pdb_reader_dll_interface": False,
        "build_32bit": False,
    }

    def requirements(self):
        # Qt6 requirement
        self.requires("qt/6.8.3")

	# Force libiconv 1.18 because default 1.17 throws an error
        # self.requires("libiconv/1.18", force=True)

        # Optional dependencies
        if self.options.build_with_fmu2_support or self.options.build_with_fmu3_support:
            self.requires("pugixml/1.14")

    def configure(self):
        # Qt6 configuration
        self.options["qt"].shared = True
        self.options["qt"].gui = True
        self.options["qt"].widgets = True
        self.options["qt"].qttools = True

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        
        # Pass our options to CMake
        tc.variables["BUILD_EXAMPLES"] = self.options.build_examples
        tc.variables["BUILD_WITH_FMU2_SUPPORT"] = self.options.build_with_fmu2_support
        tc.variables["BUILD_WITH_FMU3_SUPPORT"] = self.options.build_with_fmu3_support
        tc.variables["BUILD_ESMINI_EXAMPLE"] = self.options.build_esmini_example
        tc.variables["BUILD_WITH_J1939_SUPPORT"] = self.options.build_with_j1939_support
        tc.variables["BUILD_WITH_GATEWAY_VIRTUAL_CAN"] = self.options.build_with_gateway_virtual_can
        tc.variables["BUILD_WITH_PDB_READER_DLL_INTERFACE"] = self.options.build_with_pdb_reader_dll_interface
        tc.variables["BUILD_32BIT"] = self.options.build_32bit
        
        # Set CMake generator to Ninja
        tc.generator = "Ninja"
        
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        # Copy license and documentation
        copy(self, "LICENSE*", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, "README*", dst=os.path.join(self.package_folder, "doc"), src=self.source_folder)
