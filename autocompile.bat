@echo off

cxFreeze main.py --target-dir Dist --icon favicon.ico --include-msvcr --base-name=win32gui
iscc .\DistISS\setupScript.iss