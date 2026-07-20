# Palette's UX and Accessibility Journal

## 2025-07-20 - Multi-Modal Telemetry & Clean CustomTkinter Lifecycles
**Learning:** Telemetry HUDs that rely solely on color transitions (e.g., green to red) to represent warning thresholds violate WCAG 1.4.1 (Use of Color) and exclude colorblind users. Adding distinct, high-contrast emoji indicators (🟢 vs 🚨) ensures immediate status clarity. Additionally, running background updates via CustomTkinter's `.after()` can cause memory leaks or threading crashes upon window closure if scheduled jobs are not properly stored and cancelled with `after_cancel()` in an overridden `destroy()` method. Finally, adding keybinds like Escape to utility HUDs significantly enhances keyboard-only accessibility.
**Action:** For every CustomTkinter telemetry window, always:
1. Couple color updates with unmistakable emojis or text symbols (🟢 vs 🚨).
2. Override `destroy()` to clear any active `.after()` scheduled IDs using `after_cancel()`.
3. Bind `<Escape>` to the teardown of topmost tool window interfaces.
