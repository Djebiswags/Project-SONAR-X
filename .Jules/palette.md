# Palette's Journal - Critical Learnings

## 2025-02-18 - Colorblind Friendly HUD Indicators
**Learning:** WCAG 1.4.1 requires that color is not used as the sole visual means of conveying information. When designing real-time HUDs with threshold-based states (e.g., high CPU load redline warnings), combining color changes with text updates, distinct icons, or accessibility indicators ensures information is accessible to colorblind users.
**Action:** Always combine status color shifts with unique textual cues, emoji indicators (such as 🟢 and 🚨), or other distinct symbols to differentiate states clearly without relying on color alone.

## 2025-02-18 - Keyboard Accessibility in Utility Windows
**Learning:** For floating or utility-style HUD windows, keyboard-only users need quick and intuitive ways to dismiss them. Binding the Escape key globally allows rapid closing.
**Action:** Bind the Escape key to close topmost utility windows to ensure keyboard navigation remains smooth and efficient.

## 2025-02-18 - Preventing Memory Leaks from Recurring Scheduled Events
**Learning:** Scheduling recurring updates in CustomTkinter via `.after()` can cause memory leaks, background processing overhead, or Tcl/threading errors if the window is destroyed but the callback continues to run.
**Action:** Always store the scheduled job ID and override the `destroy()` method to cancel pending callbacks via `after_cancel()` upon teardown.
