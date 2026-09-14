## 2025-05-18 - WCAG Multi-Modal Telemetry & Global Shortcut Binding
**Learning:** Highlighting telemetry state changes using color alone fails WCAG 1.4.1 for colorblind users, and utility windows like HUDs need global keyboard shortcuts (`bind_all("<Escape>")`) to ensure dismissability regardless of component focus.
**Action:** Combine color updates with explicit visual indicators (like 🟢/🚨) and use `bind_all` for window dismiss shortcuts in Tkinter/CustomTkinter apps.
