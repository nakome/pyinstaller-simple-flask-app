# pyinstaller-simple-flask-app

Simple desktop app made with flask ( only test on llinux )


### Requirements

- Python
- PySide
- Flask
- PyInstaller


### Test

    python3 start.py

## spec settings

    # App name
    AppName = 'MyApp' # if change app name be sure to change appName on __init__.py
    # App dir only try on linux :(
    AppDir = '/home/jhon/Documents/pyinstaller-simple-flask-app'
    # File to init app
    AppFileInit = 'start.py'
    # icon file bug :(
    icoFile = 'app/static/icon.png'

### build
    pyinstaller makeApp.spec


