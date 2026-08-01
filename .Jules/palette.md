# Palette's Journal

## 2025-02-14 - Multi-modal telemetry indicators & keyboard accessibility
**Learning:** For utility windows and telemetry HUDs, relying only on color changes to indicate warning levels (like red for high CPU load) is insufficient and violates WCAG 1.4.1 (Use of Color). Combining color changes with distinct emojis (e.g., 🟢 and 🚨) ensures the UI is accessible for colorblind users. Additionally, keyboard accessibility can be drastically improved by binding the Escape key globally via `bind_all` so that users can instantly close auxiliary utility windows without needing to grab their mouse.
**Action:** Always pair visual indicators with textual or emoji counterparts, and provide quick global key bindings (e.g., Escape) on utility dashboards. Overriding `destroy()` to cleanly cancel scheduled `.after()` jobs ensures no memory leaks or thread/Tcl crashes when the window is dismissed.
