# Palette's UX Journal

## 2025-05-18 - WCAG 1.4.1 Multi-Modal Telemetry & Window Dismissal
**Learning:** System telemetry HUDs that rely solely on text color changes (e.g. green vs red) fail WCAG 1.4.1 for colorblind users, and persistent top-most utility windows require instant keyboard dismissal (<Escape>) to prevent user disruption.
**Action:** Always combine status colors with clear visual icons/emojis (🟢 vs 🚨) and bind global keyboard shortcuts (`bind_all("<Escape>")`) to close utility overlays.
