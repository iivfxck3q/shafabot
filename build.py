import PyInstaller.__main__
import os
import platform

import os
import shutil

FILES = ['app.exe', 'app.spec']
FOLDERS = ['build']


def __delete(lists, folder=False):
    try:
        for _ in lists:
            if folder == False:
                os.remove(_)
            else:
                shutil.rmtree(_)
    except:
        pass


def start_build():
    __delete(FILES)
    __delete(FOLDERS, True)
    PyInstaller.__main__.run([
        'app.py',
        '--onefile',
        '--clean',
        '--upx-dir=upx/',
        '--distpath=.',
    ])

    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    print("Сборка завершена!")
    __delete(FOLDERS, True)


if __name__ == "__main__":
    start_build()
