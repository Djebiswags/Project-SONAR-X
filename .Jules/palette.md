# Palette's UX/A11y Journal

## 2025-07-23 - CustomTkinter Multi-Modal Indicators & Safe Teardown
**Learning:** In CustomTkinter or Tkinter telemetry dashboards, relying only on text color transitions violates WCAG 1.4.1 (Use of Color). Colorblind users cannot distinguish warning states (e.g. Red vs. Turquoise) without additional visual indicators like emojis (🟢 and 🚨). Additionally, using `.after()` for periodic telemetry polling can cause memory leaks and threading errors on teardown if the job ID is not stored and canceled with `after_cancel()` when the widget is destroyed.
**Action:** Always pair color changes with distinct status emojis (e.g., 🟢 and 🚨) for accessibility, override the `destroy` method of the main window class to cancel any pending `after` callback loops, and bind the Escape key (`<Escape>`) to `self.destroy` for keyboard-accessible closing.
