# Palette's Journal

🎨 A log of critical UX and accessibility learnings.

## 2025-02-18 - Multi-modal Telemetry Visual Cues & HUD Keyboard Close
**Learning:** In telemetry HUD dashboards and system utility windows, relying purely on color transitions (e.g., turning a label from green to red to flag high CPU usage) violates WCAG Guideline 1.4.1 (Use of Color). Users with color vision deficiencies cannot reliably perceive these status changes. Additionally, floating telemetry windows often lack simple, intuitive keyboard dismissals, creating friction for keyboard-only users.
**Action:** Always pair status-driven color changes with clear visual symbols or textual indicators (such as 🟢 and 🚨 emojis) to ensure multi-modal accessibility. Additionally, ensure floating helper windows or HUDs are instantly dismissible by binding the `<Escape>` key to close the window.
