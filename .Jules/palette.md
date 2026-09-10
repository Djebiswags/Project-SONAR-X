## 2026-05-18 - WCAG 1.4.1 Multi-Modal HUD Telemetry & Keyboard Dismissal in CustomTkinter

**Learning:** Telemetry HUD overlays relying solely on color changes for status updates (e.g., green to red for CPU load) violate WCAG 1.4.1 (Use of Color) and create barriers for colorblind users. Additionally, utility overlay windows in Tkinter/CustomTkinter require global keybindings (`bind_all`) for standard keyboard dismissals like `<Escape>` to handle focus unpredictability.

**Action:** Combine color changes with distinct status emojis/symbols (e.g., 🟢 normal vs 🚨 high) for multi-modal visual cues, bind `<Escape>` globally using `bind_all("<Escape>", ...)` to dismiss HUD overlays, and cancel recurring `after()` job IDs in `destroy()` to prevent memory leaks and Tcl errors.
