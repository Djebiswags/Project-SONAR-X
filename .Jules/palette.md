## 2025-08-04 - Multi-Modal Telemetry and Keyboard Accessibility in CustomTkinter HUDs
**Learning:**
1. Adherence to WCAG 1.4.1 (Use of Color) on real-time telemetry HUDs is achieved by combining status color transitions with multi-modal visual markers (such as emojis like 🟢 and 🚨). This guarantees that colorblind users can instantly distinguish status states without relying purely on color differences.
2. In CustomTkinter or Tkinter applications, global keyboard shortcuts (like using the Escape key to close utility or floating windows) should be bound using `bind_all` rather than instance-level `bind` to ensure that keystrokes are registered regardless of which sub-widget has focus.
3. Recurring updates scheduled via `.after()` must store their job IDs and be cancelled explicitly via `after_cancel()` when the widget or window is destroyed to avoid memory leaks, dangling handlers, and runtime Tcl errors during teardown.

**Action:**
- In all desktop/Tkinter HUD utilities, implement multi-modal indicators (emojis/text) alongside colors.
- Use `bind_all("<Escape>", ...)` to enable universal keyboard exit.
- Override `destroy()` to clear scheduled tasks using `after_cancel()`.
