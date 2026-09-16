## 2026-05-18 - Multi-modal telemetry indicators and HUD window dismissal

**Learning:** Relying solely on color changes (e.g. green to red) for CPU threshold alerts in CustomTkinter HUD displays violates WCAG 1.4.1 (Use of Color). Combining color changes with distinct status icons (e.g. 🟢 vs 🚨) improves accessibility for colorblind users. Additionally, utility overlay windows in Tkinter/CustomTkinter should have global keybindings (`bind_all('<Escape>')`) and teardown hooks (`after_cancel`) to guarantee keyboard dismissability and clean timer cancellation.

**Action:** Always include multi-modal status indicators alongside color alerts and bind the Escape key globally on desktop HUD overlay windows.
