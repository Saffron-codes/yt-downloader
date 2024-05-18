#!/bin/bash

if ! command -v pyinstaller &> /dev/null
then
    pip install pyinstaller
fi

pyinstaller --onefile src/main.py

if [ $? -eq 0 ]; then
    echo "PyInstaller finished successfully."
else
    echo "PyInstaller encountered an error."
fi
