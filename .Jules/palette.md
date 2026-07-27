# Palette's UX Journal

This journal tracks critical UX and accessibility learnings from working on Project SONAR-X.

## 2025-02-15 - [Multimodal Indicators & Keyboard Accessibility in Desktop HUDs]
**Learning:** Purely color-based status indicators (e.g. green vs. red text) violate WCAG 1.4.1 (Use of Color), presenting barriers to colorblind users. Combining colors with distinct visual symbols or emojis (e.g., 🟢, 🚨, ⏳) provides a robust multimodal indicator. Additionally, utility desktop windows should support the Escape key globally to allow immediate and easy dismissal via keyboard-only navigation.
**Action:** When designing status or telemetry HUDs, always pair color indicators with distinct symbols/text prefixes, and bind Escape using `bind_all` globally to ensure it functions regardless of which sub-widget holds keyboard focus.
