# Palette's UX & Accessibility Journal

## 2025-02-14 - Multi-Modal Telemetry & Clean Tkinter Teardowns
**Learning:** For status telemetry displays (such as live CPU and RAM stats), changing label color alone (e.g., green to red) to indicate state violations violates WCAG 1.4.1 (Use of Color). We must use multi-modal feedback like distinct emojis (🟢 and 🚨) or text indicators alongside color to assist colorblind and low-vision users. Additionally, in CustomTkinter/Tkinter applications, global keyboard actions (like closing utility HUD windows with Escape) should be bound globally with `bind_all` rather than locally to capture inputs when any sub-widget is focused. Lastly, to prevent memory leaks and threading/Tcl errors on teardown when scheduling recurring updates via `.after()`, the scheduled job ID must be stored and cancelled via `after_cancel()` in an overridden `destroy()` method.
**Action:** Always combine telemetry color shifts with emojis or text icons, bind utility close/exit shortcuts globally with `bind_all`, and override `destroy()` to cancel scheduled `.after()` jobs in Tkinter apps.

## 2025-02-14 - Programmatic Headless Focus Testing
**Learning:** Testing keyboard events programmatically in headless Xvfb environments requires ensuring that the focus is correctly directed to the window. Calling `hud.event_generate('<Key-Name>')` on a headless tkinter instance will only trigger focus-bound shortcuts if `hud.deiconify()`, `hud.focus_force()`, and `hud.update()` are executed beforehand to properly flush the X11 window queue and activate window focus.
**Action:** Use `deiconify()`, `focus_force()`, and `update()` before simulating keyboard shortcuts in Tkinter/CustomTkinter unit tests.
