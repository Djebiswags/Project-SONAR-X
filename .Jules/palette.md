## 2025-02-12 - [Accessible & Leak-Free CustomTkinter HUDs]
**Learning:**
1. Adhering to WCAG 1.4.1 (Use of Color) is crucial in desktop telemetries where green/red indicators (like safe vs overload states) are used. Supplementing color changes with multi-modal visual indicators (such as distinct emojis like 🟢 and 🚨) ensures that colorblind users can immediately identify critical status changes.
2. For keyboard accessibility, global bindings must be used. In Tkinter and CustomTkinter, global keyboard shortcuts (such as using the Escape key to close utility/HUD windows) must be bound using `bind_all` instead of instance-level `bind` so that they are reliably triggered even if focus is currently captured by inner sub-widgets.
3. Scheduling UI updates via `.after()` in CustomTkinter windows can cause memory leaks, thread/Tcl errors, and unexpected crashes upon teardown if the scheduled callback is still pending when the window is destroyed. It is imperative to capture the schedule ID and cancel any outstanding scheduled callbacks with `after_cancel()` by overriding the window's `destroy()` method.

**Action:**
- Always couple color-based status indicators with semantic emojis or symbols.
- Use `self.bind_all("<Escape>", ...)` to handle keyboard shortcuts for modal and utility/HUD windows.
- Always store `.after()` job IDs and call `after_cancel()` in `destroy()` when using Tkinter/CustomTkinter.
