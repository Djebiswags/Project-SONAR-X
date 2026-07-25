# Palette's UX Journal

## 2023-11-20 - Multi-modal indicators and Keyboard Access in CustomTkinter HUD
**Learning:** For telemetry HUDs, relying purely on color changes (like cyan/red for CPU warning status) fails WCAG 1.4.1 (Use of Color) for colorblind users. Combining color changes with distinct text/emojis (e.g., 🟢 and 🚨) ensures visual accessibility. Additionally, binding the Escape key provides a standard, intuitive mechanism for keyboard-only users to close utility windows. Overriding `destroy()` to clean up scheduled `.after()` jobs prevents Tcl and threading issues on exit.
**Action:** Always pair telemetry color status with textual/emoji indicators, bind the Escape key, and properly cancel scheduled GUI update IDs upon widget destruction in Tkinter/CustomTkinter apps.
