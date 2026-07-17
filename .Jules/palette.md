# Palette's Journal

## 2025-02-18 - [HUD Accessibility & Memory Management in CustomTkinter]
**Learning:** For telemetry HUDs and utility windows built with CustomTkinter, adhering to WCAG 1.4.1 (Use of Color) is critical. We must combine color changes with multi-modal visual indicators (such as emojis or text labels) to assist colorblind users. Additionally, keyboard accessibility (binding 'Escape' key to close windows) is important for UX comfort. Finally, to prevent memory leaks and threading/Tcl errors on teardown when scheduling recurring telemetry or UI updates via `.after()`, we should store the scheduled job ID and cancel it via `after_cancel()` in an overridden `destroy()` method.
**Action:** Always store job IDs when using `.after()`, cancel them in `destroy()`, bind 'Escape' to close the utility window, and add multi-modal status indicators alongside color-coding.
