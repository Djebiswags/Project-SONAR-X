# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-02-13 - [Multi-Modal CustomTkinter Telemetry & Keyboard Accessibility]
**Learning:** For telemetry HUDs and utility windows, relying purely on color (like red/cyan text) to indicate high resource utilization violates WCAG 1.4.1 (Use of Color). Colorblind users need a multi-modal visual indicator (like emojis 🟢/🚨) alongside the color change. Furthermore, utility windows should be keyboard-accessible by binding the Escape key globally via `bind_all` (rather than instance `bind`) so that focus issues do not prevent the shortcut from working. Lastly, to prevent Tcl threading errors and memory leaks, any scheduled `.after()` updates must have their ID saved and cancelled in `destroy()`.
**Action:** Always combine telemetry color changes with distinct emojis/icons, bind key shortcuts using `bind_all`, and explicitly cancel scheduled tkinter jobs during clean-up.
