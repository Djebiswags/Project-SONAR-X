## 2026-08-25 - Multi-Modal Telemetry & Keyboard Dismissal for Tkinter HUDs

**Learning:** When presenting status changes (like CPU redline alerts) in CustomTkinter HUDs, color changes alone fail WCAG 1.4.1 (Use of Color) for colorblind users. Combining text colors with multi-modal visual status indicators (🟢 vs 🚨) ensures universal status clarity. Additionally, utility windows should always bind `<Escape>` globally using `bind_all` and cleanly cancel recurring `after()` timers on `destroy()` to prevent memory leaks or Tcl callbacks after teardown.

**Action:** Always include non-color status indicators alongside text color changes in dashboard telemetry labels, bind `<Escape>` via `bind_all`, and store/cancel `after()` timers in `destroy()`.
