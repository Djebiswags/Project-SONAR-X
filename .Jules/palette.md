# Palette's Journal

## 2025-02-17 - [Multi-modal and Keyboard Accessibility in telemetry HUDs]
**Learning:** Resource-monitoring HUDs (like `dashboard.py`) often rely purely on color-coding (e.g. green to red) to indicate status changes. This violates WCAG Guideline 1.4.1 (Use of Color), making it inaccessible to colorblind users. Additionally, utility HUDs on macOS are often set to "always on top" (`-topmost True`), which makes them intrusive if they cannot be dismissed rapidly via keyboard shortcuts.
**Action:** Always provide a non-color visual indicator (such as warning emojis or text status) alongside color changes, and bind standard escape shortcuts (like `Escape` key) to quickly close topmost utility windows.
