# Palette's Journal - Critical UX/Accessibility Learnings

This journal documents critical learnings on UX and accessibility enhancements for Project SONAR-X.

## 2024-07-19 - [Multi-modal Visual Indicators & Keyboard Accessibility in Telemetry HUDs]
**Learning:** Under WCAG 1.4.1 (Use of Color), color alone should not be used to convey information or distinguish elements. Combining color changes (e.g., green vs. red) with distinct emojis (e.g., 🟢 and 🚨) provides a multi-modal visual indicator that is accessible to colorblind and visually impaired users. Furthermore, utility windows and HUDs must support keyboard accessibility, such as binding the Escape key to quickly close the window for keyboard-only users.
**Action:** Always pair status/severity color states with textual or symbolic indicators (emojis, labels, icons) and ensure proper keyboard listeners exist for seamless window/HUD teardown and dismissal.
