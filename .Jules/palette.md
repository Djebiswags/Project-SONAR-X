## 2026-03-30 - Multi-modal indicators for telemetry HUDs
**Learning:** Color-only status changes (e.g. green to red CPU text) fail WCAG 1.4.1 (Use of Color) for colorblind users and lack immediate clarity for screen reader users. Combining multi-modal status emojis (🟢 / 🚨) with global Escape key dismiss functionality improves both visual accessibility and keyboard usability for overlay utility windows.
**Action:** Always combine status colors with visual indicators/emojis and bind `bind_all('<Escape>')` for quick window dismissal in desktop HUD components.
