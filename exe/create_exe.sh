#!/bin/bash

# info:
# - paths are relative to the main folder of the repository

# variables
venv="venv_tmp_exe"
name="app_openai_main"

# check existence of exe/$name
if [ -d "exe/$name" ]; then
    echo "Error: "exe/$name" already exist."
    exit 1
fi

# check existence of $venv
if [ -d $venv ]; then
    echo "Error: $venv already exist."
    exit 1
fi

# venv: create and activate
python -m venv $venv
. "$venv/Scripts/activate"

# pip install
pip install -r "requirements.txt"
pip install pyinstaller
pip install pywin32

# pyinstaller
pyinstaller --noconfirm --onedir --windowed \
    --icon "img/image_default.ico" \
    --add-data "$venv/Lib/site-packages/customtkinter;customtkinter/" \
    --distpath "exe" \
    "src/$name.py"

# copy and delete folders
rm -rf "build"
rm -rf "$name.spec"
cp -r "doc" "exe/$name/doc"
cp -r "img" "exe/$name/img"
cp "api.key" "exe/$name/api.key"

# venv: deactivate and delete
deactivate
rm -rf "$venv"
