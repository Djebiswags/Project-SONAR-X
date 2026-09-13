## 2026-03-31 - Multi-modal indicators and Escape shortcut for Tkinter HUDs
**Learning:** For telemetry HUDs and utility windows, color changes alone fail WCAG 1.4.1 for colorblind accessibility. Combining status colors with distinct visual indicators (like 🟢 and 🚨) improves visual clarity. Additionally, global keybindings (`bind_all("<Escape>")`) allow users to quickly dismiss utility overlays without needing mouse interaction.
**Action:** Always combine status colors with multi-modal icons/indicators and provide `<Escape>` keyboard shortcuts on utility HUD overlays.
