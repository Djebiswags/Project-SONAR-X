# Palette's UX & Accessibility Journal

## 2025-02-15 - [Tkinter/CustomTkinter Robust Keyboard Accessibility & Teardown Lifecycle]
**Learning:**
1. In CustomTkinter applications, global keyboard shortcuts (like `Escape` to close the HUD utility window) must be bound using `bind_all` rather than widget-level `bind` to ensure events are captured even when a sub-widget (like a label or button) has keyboard focus.
2. Scheduling continuous GUI updates via `.after()` creates persistent timer references. If the window is destroyed without canceling these jobs, it causes background threads to keep running or raises Tcl errors on teardown. Overriding `destroy()` to call `after_cancel()` gracefully prevents resource leaks and thread warnings.
3. Testing keyboard events programmatically in headless Linux environments (with Xvfb) requires explicitly calling `deiconify()`, `focus_force()`, and `update()` before generating event sequences, otherwise the simulated keystrokes are ignored because of un-focused window states.

**Action:**
Always bind global shortcuts via `bind_all`, store and cancel scheduled Tkinter job IDs inside an overridden `destroy()` method on any CustomTkinter/Tkinter class, and ensure window visibility and focus are forced during programmatic headless test suites.
