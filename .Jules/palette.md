## 2025-05-18 - Multi-modal indicators and keyboard dismissal for telemetry HUDs
**Learning:** Color-only indicators (like red text for high CPU load) fail WCAG 1.4.1 (Use of Color) for colorblind users. Furthermore, utility popup HUD windows without keyboard shortcuts require mouse interaction to dismiss.
**Action:** Always combine status colors with clear visual icons (e.g. 🟢 and 🚨) in CustomTkinter labels and bind `<Escape>` via `bind_all` to allow immediate keyboard dismissal, while safely canceling scheduled `.after()` jobs in `destroy()` to prevent Tcl errors.
