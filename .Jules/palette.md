## 2026-03-31 - Telemetry HUD Multi-Modal Indicators & Key Navigation

**Learning:** Relying solely on color changes (e.g., green vs red text) for telemetry indicators violates WCAG 1.4.1 (Use of Color) and excludes colorblind users. Combining color changes with distinct status emojis (🟢 / 🚨) ensures accessibility. Additionally, floating utility HUDs need keyboard dismissal shortcuts (`Escape`) bound globally (`bind_all`) with proper cleanup (`after_cancel`, `unbind_all`) on teardown to avoid memory leaks.
**Action:** Always include non-color visual symbols alongside color changes in telemetry views, and manage `bind_all` and `after` handles in window `destroy()` methods.
