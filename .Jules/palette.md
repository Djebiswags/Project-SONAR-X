# Palette's Journal

## 2024-11-20 - [WCAG 1.4.1 compliance and Escape-key Dismissal in CustomTkinter HUD]
**Learning:** For telemetry HUDs and utility windows, relying solely on color changes (e.g. red vs cyan) for high CPU/RAM usage fails WCAG 1.4.1 (Use of Color). Combining color changes with distinct text/emoji indicators (like 🟢/🚨) provides critical visual affordances for colorblind users. Additionally, utility windows should always support keyboard dismissibility by binding the `Escape` key.
**Action:** Always combine semantic color states with non-color indicators (e.g., emojis, text prefixes) and bind the `<Escape>` key to exit/close HUD/popup windows.
