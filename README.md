## Pynotes

Simple desktop app made with flask

> This is only for experiment propouses.

### Requirements

- Python
- PySide
- Flask
- PyInstaller
- PyQt5

### Test

    python pynotes.py


### build

	
	pyinstaller -w -F --icon="pynotes.ico" --add-data "static;static" --add-data "templates;templates" pynotes.py


Copy static & templates folder on dist directory and thats it.
