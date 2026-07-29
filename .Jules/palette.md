# Palette's Journal - Project SONAR-X

## 2024-11-20 - [WCAG Multi-modal Indicators & Keyboard Escape Bindings in CustomTkinter]
**Learning:** For floating utility/HUD windows, providing immediate keyboard dismissability (via the Escape key bound globally with `bind_all`) significantly improves keyboard accessibility. Additionally, relying solely on color changes for status updates violates WCAG 1.4.1 (Use of Color). Combining color shifts with multi-modal visual cues (like distinct emojis 🟢/🚨) ensures colorblind users can immediately read the system status.
**Action:** When creating Tkinter/CustomTkinter utility HUDs, always include a global `<Escape>` binding to close the window, add emoji/status indicators beside text updates, and ensure safe lifecycle teardown by storing/canceling `.after()` job IDs inside an overridden `destroy()` method.
