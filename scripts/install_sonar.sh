#!/usr/bin/env bash
set -euo pipefail

APP_NAME="SONAR-X.app"
SRC_DIR="dist/${APP_NAME}"
DEST_DIR="/Applications/${APP_NAME}"

if [ ! -d "$SRC_DIR" ]; then
  echo "Error: built app not found at $SRC_DIR"
  exit 1
fi

echo "Copying $SRC_DIR -> $DEST_DIR"
cp -R "$SRC_DIR" "/Applications/"
echo "Installed to /Applications/${APP_NAME}"
echo "You can run it with: open /Applications/${APP_NAME}"

echo "If you want it to launch at login, install the included LaunchAgent plist manually."
echo "See README.md for details."
