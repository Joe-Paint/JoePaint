:; if [ -z 0 ]; then
  @echo off
  bash %~f0 %*
  exit /b %errorlevel%
fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd $SCRIPT_DIR

/usr/bin/python3 -m pip install --upgrade pip

REQUIRED_PACKAGES=("opencv-python" "numpy" "astropy")

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! /usr/bin/python3 -m pip show "$pkg" &> /dev/null; then
        /usr/bin/pip3 install $pkg
    fi
done
