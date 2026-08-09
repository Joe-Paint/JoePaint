:; if [ -z 0 ]; then
  @echo off
  bash %~f0 %*
  exit /b %errorlevel%
fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd $SCRIPT_DIR
/usr/bin/python3 source/main.py
