from setuptools import setup

APP = ['sonar_menu.py']
DATA_FILES = ['config.example.json', 'mac_startup_daemon.plist', 'dashboard.py', 'README.md', 'LICENSE']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['rumps', 'psutil', 'requests'],
    'packages': ['rumps', 'psutil', 'requests'],
    'plist': {
        'CFBundleName': 'SONAR-X',
        'CFBundleIdentifier': 'com.oracle.sonarx',
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': True,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
