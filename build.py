import platform
import sys
import PyInstaller.__main__

def build_executable():
    OS = platform.system()

    options = [
        'KVConversor.py',
        '--clean',
        '--onefile',
        '--runtime-tmpdir=.',
        '--icon=icon.ico',
        '--exclude-module=config'
    ]

    if OS == 'Windows':
        options.extend(['--hidden-import=pywin32', '--name=KVConversor.exe'])
    elif OS == 'Darwin':
        options.append('--name=KVConversor.command')
    elif OS == 'Linux':
        options.append('--name=KVConversor')
    else:
        print("Unsupported operating system.")
        sys.exit(1)

    PyInstaller.__main__.run(options)

if __name__ == "__main__":
    build_executable()
