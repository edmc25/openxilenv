import os
import sys
import platform
from pathlib import Path

# Make the bundled Samples/Automation Python package importable for tests.
# The OpenXilEnv Python package lives under Samples/Automation/Python/OpenXilEnv
repo_root = Path(__file__).resolve().parents[2]
pkg_path = repo_root / "Samples" / "Automation" / "Python" / "OpenXilEnv"
if str(pkg_path) not in sys.path:
    sys.path.insert(0, str(pkg_path))

import pytest
from OpenXilEnv.openXilEnv import OpenXilEnv  # now importable thanks to sys.path tweak


@pytest.fixture(scope="session")
def xilEnvInstallationPath() -> Path:
    """Path to the built OpenXilEnv installation.

    The path can be overridden using the XILENV_INSTALLATION_PATH environment variable.
    """
    env = os.environ.get("XILENV_INSTALLATION_PATH")
    if env:
        xilEnvInstallationPath = Path(env)
    else:
        system = platform.system()
        if system == "Windows":
            xilEnvInstallationPath = Path(r"d:\a\openxilenv\openxilenv\OpenXilEnv-Windows-Qt6_9_2")
        elif system == "Linux":
            xilEnvInstallationPath = Path("/home/runner/work/openxilenv/openxilenv/OpenXilEnv-Linux")
        else:
            pytest.skip(f"Unsupported platform: {system}")
            return None
    
    assert xilEnvInstallationPath.is_dir(), f"no such directory {xilEnvInstallationPath}"
    return xilEnvInstallationPath


@pytest.fixture(scope="session")
def iniFilePath() -> Path:
    """Path to the ElectricCarSample.ini used by the functional tests.

    The path can be overridden using the ELECTRIC_CAR_INI environment variable.
    """
    env = os.environ.get("ELECTRIC_CAR_INI")
    if env:
        iniFilePath = Path(env)
    else:
        system = platform.system()
        if system == "Windows":
            iniFilePath = Path(r"d:\a\openxilenv\openxilenv\openxilenv\Samples\Configurations\ElectricCarSample.ini")
        elif system == "Linux":
            iniFilePath = Path("/home/runner/work/openxilenv/openxilenv/openxilenv/Samples/Configurations/ElectricCarSample.ini")
        else:
            pytest.skip(f"Unsupported platform: {system}")
            return None
    
    assert iniFilePath.is_file(), f"no such file {iniFilePath}"
    return iniFilePath
