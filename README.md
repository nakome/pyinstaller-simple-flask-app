# pyinstaller-simple-flask-app

Simple desktop app made with flask ( only test on llinux )


### Requirements

- Python
- Flask
- PyInstaller


### Test 

    python3 start.py

## spec settings

    # App name
    AppName = 'MyApp'
    # App dir only try on linux :(
    AppDir = '/home/jhon/Documents/pyinstaller-simple-flask-app'
    # File to init app
    AppFileInit = 'start.py'
    # icon file bug :(
    icoFile = 'app/static/icon.png'

### build
    pyinstaller makeApp.spec


