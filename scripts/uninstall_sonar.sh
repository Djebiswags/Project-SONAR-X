#!/usr/bin/env bash
set -euo pipefail

APP_PATH="/Applications/SONAR-X.app"

echo "Stopping running SONAR-X processes (if any)"
pkill -f SONAR-X || true

if [ -d "$APP_PATH" ]; then
  echo "Removing $APP_PATH"
  rm -rf "$APP_PATH"
else
  echo "$APP_PATH not present"
fi

echo "Removing Application Support data"
rm -rf "$HOME/Library/Application Support/🎧 SONAR-X" || true

echo "Unloading and removing LaunchAgent plist (if present)"
launchctl unload ~/Library/LaunchAgents/com.oracle.sonarx.plist 2>/dev/null || true
rm -f ~/Library/LaunchAgents/com.oracle.sonarx.plist || true

echo "Uninstall complete."
