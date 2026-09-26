## 2025-05-18 - Multi-Modal Telemetry Status and CustomTkinter HUD Teardown

**Learning:** Relying solely on color changes (e.g. green vs red text) to communicate state changes in live telemetry windows violates WCAG 1.4.1 (Use of Color) and impairs colorblind users. Combining distinct status icons/emojis (🟢/🚨) with text and color allows non-visual and colorblind users to immediately differentiate standard load from alert states. Additionally, binding global keyboard shortcuts (`bind_all`) for window dismissal requires explicitly cancelling scheduled `.after()` jobs and unbinding global key handlers upon window destruction to prevent memory leaks and Tcl callback exceptions.

**Action:** Always combine color changes with distinct multi-modal visual indicators (such as status emojis) when displaying status/telemetry alerts, and ensure CustomTkinter windows override `destroy()` to cancel `.after()` timers and `unbind_all()` keyboard shortcuts.
