# Palette's Journal - Project SONAR-X UX & Accessibility

This journal tracks critical UX/accessibility insights and learnings for Project SONAR-X.

## 2025-07-18 - CustomTkinter Telemetry & Keyboard Accessibility
**Learning:** For floating HUD dashboards or utility windows built using CustomTkinter, keyboard accessibility (WCAG 2.1) and screen-agnostic indicators (WCAG 1.4.1) are critical. Simply relying on color changes (e.g. red vs green/teal) fails to assist colorblind users. Combining color changes with multi-modal visual indicators (such as 🟢 and 🚨 emojis) provides immediate visual clarity. Additionally, topmost utility windows should always bind the `Escape` key to close the window, allowing keyboard-only users to dismiss the interface cleanly. Furthermore, to avoid threading/Tcl errors or memory leaks during window teardown, any scheduled `.after()` jobs must be stored and cancelled via `self.after_cancel()` inside an overridden `destroy()` method.
**Action:** Apply Escape key binding (`<Escape>`), multi-modal emojis (🟢 / 🚨), and a proper teardown lifecycle (`after_cancel` in `destroy`) to telemetry HUD windows in CustomTkinter.
