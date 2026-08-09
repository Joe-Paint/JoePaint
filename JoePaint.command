SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd $SCRIPT_DIR
/usr/bin/python3 source/main.py
