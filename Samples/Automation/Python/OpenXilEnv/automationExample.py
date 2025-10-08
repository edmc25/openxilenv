from OpenXilEnv.openXilEnv import OpenXilEnv
import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        prog="automationExample.py",
        description="Run a small OpenXilEnv automation example. Accepts either positional arguments or uses the defaults in the script."
    )
    parser.add_argument(
        "installation_path",
        nargs="?",
        help="Path to XilEnv installation (directory or executable). If omitted the script default is used.",
        default=None,
    )
    parser.add_argument(
        "ini_file",
        nargs="?",
        help="Path to ElectricCarSample.ini. If omitted the script default is used.",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Don't check that provided paths exist; useful for dry runs or when placeholders are used.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Keep the original placeholder defaults if the user doesn't provide values.
    xilEnvInstallationPath = args.installation_path or "path/to/xil/installation"
    electricCarIniFilePath = args.ini_file or "path/to/ElectricCarSample.ini"

    # Basic validation (can be skipped with --force)
    if not args.force:
        if not os.path.exists(xilEnvInstallationPath):
            print(
                f"Error: installation path not found: {xilEnvInstallationPath}",
                file=sys.stderr,
            )
            sys.exit(2)
        if not os.path.exists(electricCarIniFilePath):
            print(
                f"Error: INI file not found: {electricCarIniFilePath}",
                file=sys.stderr,
            )
            sys.exit(2)

    xil = OpenXilEnv(xilEnvInstallationPath)
    xil.startWithGui(electricCarIniFilePath)

    xil.attachVariables(["FireUp", "PlugIn"])

    xil.writeSignal("FireUp", 1)
    cycles = xil.waitUntilValueMatch("FireUp", 1, 1)
    print(f"Remaining cycles: {cycles}")
    print(f"FireUp: {xil.readSignal('FireUp')}")

    xil.writeSignal("FireUp", 0)
    cycles = xil.waitUntilValueMatch("FireUp", 0, 1)
    print(f"Remaining cycles: {cycles}")
    print(f"FireUp: {xil.readSignal('FireUp')}")

    xil.disconnectAndCloseXil()


if __name__ == "__main__":
    main()
