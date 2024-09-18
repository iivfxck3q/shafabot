import subprocess
import sys


def setup():
    packages = [
        "pyinstaller",
        "flet",
        "selenium",
        "tabulate",
        "bs4",
        "requests",
        "pillow"
    ]

    subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)


if __name__ == "__main__":
    setup()
