## 2026-08-30 - Multi-Modal Telemetry Indicators and Global Escape Binding
**Learning:** Color-only status changes in telemetry HUDs fail WCAG 1.4.1 for colorblind users; pairing status colors with distinct visual indicators (like 🟢/🚨) and binding `<Escape>` globally using `bind_all` ensures both visual and keyboard accessibility.
**Action:** Always combine status colors with non-color indicators (emojis/text icons) and use `bind_all("<Escape>")` on CustomTkinter utility windows.
