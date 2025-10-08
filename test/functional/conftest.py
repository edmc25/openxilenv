import pytest
from OpenXilEnv.openXilEnv import OpenXilEnv
from pathlib import Path

@pytest.fixture(scope="session")
def xilEnvInstallationPath() -> OpenXilEnv:
    xilEnvInstallationPath = Path("d:\\a\\openxilenv\\openxilenv\\OpenXilEnv-Windows-Qt6_9_2")
    assert xilEnvInstallationPath.is_dir(), f"no such directory {xilEnvInstallationPath}"
    return xilEnvInstallationPath

@pytest.fixture(scope="session")
def iniFilePath() -> Path:
    iniFilePath = Path("d:\\a\\openxilenv\\openxilenv\\openxilenv\\Samples\\Configurations\\ElectricCarSample.ini")
    assert iniFilePath.is_file(), f"no such directory {iniFilePath}"
    return iniFilePath