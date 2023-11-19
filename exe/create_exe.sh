#!/bin/bash

# info:
# - paths are relative to the main folder of the repository

# variables
VENV="venv_tmp_exe"
NAME="app_openai_main"

# check existence of exe/$NAME
if [ -d "exe/$NAME" ]; then
echo "Error: "exe/$NAME" already exist."
exit 1
fi

# check existence of $VENV
if [ -d $VENV ]; then
echo "Error: $VENV already exist."
exit 1
fi

# venv: create and activate
python -m venv $VENV
. "$VENV/Scripts/activate"

# pip install
pip install -r "requirements.txt"
pip install pyinstaller
pip install pywin32

# pyinstaller
pyinstaller --noconfirm --onedir --windowed \
    --icon "img/image_default.ico" \
    --add-data "$VENV/Lib/site-packages/customtkinter;customtkinter/" \
    --distpath "exe" \
    "src/$NAME.py"

# copy and delete folders
rm -rf "build"
rm -rf "$NAME.spec"
cp -r "doc" "exe/$NAME/doc"
cp -r "img" "exe/$NAME/img"
cp "api.key" "exe/$NAME/api.key"

# venv: deactivate and delete
deactivate
rm -rf "$VENV"
