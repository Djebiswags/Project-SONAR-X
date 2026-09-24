## 2026-03-30 - Multi-modal indicators & Keyboard Teardown for Telemetry HUDs
**Learning:** Color alone (e.g. green vs red) is insufficient for high CPU/RAM alert indicators under WCAG 1.4.1. Combining visual emoji status indicators (🟢 vs 🚨) with global Escape key bindings (`bind_all`) dramatically improves colorblind usability and keyboard navigation in utility HUD windows.
**Action:** Always combine text status symbols with color changes on live metrics, and ensure `destroy()` cleans up `.after()` timers and `bind_all` handlers to avoid lingering Tcl callbacks.
