## 2025-02-20 - Multi-modal indicators & Escape shortcut in CustomTkinter HUD
**Learning:** In CustomTkinter utility HUDs, color changes alone for telemetry thresholds (e.g. CPU > 80%) fail WCAG 1.4.1 for colorblind users. Combining color changes with status emojis (🟢 / 🚨) and binding `<Escape>` via `bind_all` provides accessible multi-modal feedback and instant keyboard dismissibility.
**Action:** Always combine color threshold styling with clear icon/emoji indicators and bind `<Escape>` globally for floating/utility windows.
