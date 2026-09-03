## 2026-07-22 - Multi-modal Telemetry Indicators & Escape Shortcut for Utility Windows
**Learning:** Color-only telemetry alerts fail WCAG 1.4.1 (Use of Color) for colorblind users and offer no keyboard dismissal option when unfocused.
**Action:** Always combine telemetry text color changes with distinct emojis (🟢 / 🚨) and bind `<Escape>` globally using `bind_all` to allow fast keyboard dismissal of utility HUDs.
