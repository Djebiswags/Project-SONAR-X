## 2026-03-31 - Multi-modal indicators & Escape key dismiss in CustomTkinter HUD
**Learning:** For telemetry HUDs, combining text color changes with visual status icons (🟢 / 🚨) satisfies WCAG 1.4.1 (Use of Color). Binding `<Escape>` via `bind_all` ensures window dismissal works regardless of sub-widget focus, and cancelling active `.after()` schedules in `destroy()` prevents memory leaks or Tcl errors on window exit.
**Action:** Always include multi-modal icons for status changes, global keybindings with `bind_all`, and explicitly cancel scheduled TK timers in `destroy()`.
