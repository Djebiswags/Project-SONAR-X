#!/usr/bin/env bash
#set -euo pipefail

# Template: codesign and notarize SONAR-X.app
# Requirements:
# - Developer ID Application certificate installed in your login keychain
# - Xcode command-line tools installed
# - An App Store Connect API key (.p8) or Apple ID credentials for notarytool
# - This script does NOT embed secrets; set env vars before running

APP_NAME="SONAR-X.app"
APP_PATH="dist/${APP_NAME}"
DMG_PATH="dist/SONAR-X-signed.dmg"

if [ ! -d "$APP_PATH" ]; then
  echo "Built app not found at $APP_PATH"
  exit 1
fi

# Codesign (assumes certificate in keychain named "$DEVELOPER_ID_APPLICATION")
if [ -z "${DEVELOPER_ID_APPLICATION:-}" ]; then
  echo "Set DEVELOPER_ID_APPLICATION (certificate name). Example: \"Developer ID Application: Your Name (TEAMID)\""
  exit 1
fi

echo "Codesigning $APP_PATH with: $DEVELOPER_ID_APPLICATION"
# Use --deep and --options runtime for hardened runtime where appropriate
codesign --verbose --force --deep --options runtime --sign "$DEVELOPER_ID_APPLICATION" "$APP_PATH"

# Create DMG of the signed app
rm -f "$DMG_PATH"
hdiutil create -volname "SONAR-X" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_PATH"

# Notarize using xcrun notarytool (preferred). Provide either API key params or Apple ID username + password (app-specific pw).
# Example (API key):
# export NOTARY_KEY=/path/to/AuthKey_ABCDEF1234.p8
# export NOTARY_KEY_ID=ABCDEF1234
# export NOTARY_ISSUER_ID=11111111-2222-3333-4444-555555555555

if [ -n "${NOTARY_KEY:-}" ] && [ -n "${NOTARY_KEY_ID:-}" ] && [ -n "${NOTARY_ISSUER_ID:-}" ]; then
  echo "Submitting $DMG_PATH for notarization using API key"
  xcrun notarytool submit "$DMG_PATH" --key "$NOTARY_KEY" --key-id "$NOTARY_KEY_ID" --issuer "$NOTARY_ISSUER_ID" --wait
  xcrun stapler staple "$DMG_PATH"
  echo "Notarization complete. Stapled to $DMG_PATH"
else
  echo "NOTARY_KEY/NOTARY_KEY_ID/NOTARY_ISSUER_ID not set. Skipping notarization step."
  echo "You can notarize manually or set the environment vars and rerun."
fi

echo "Signed DMG available at: $DMG_PATH"
