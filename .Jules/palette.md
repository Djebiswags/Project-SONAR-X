## 2025-02-15 - Multi-Modal HUD States in CustomTkinter (WCAG 1.4.1 Compliance)
**Learning:** Purely color-coded state transitions (such as changing text color to indicate resource warning thresholds) violate WCAG 1.4.1 "Use of Color" and fail to communicate critical telemetry changes to colorblind users. Combining color transitions with distinct emojis (e.g., 🟢 and 🚨) provides an accessible, multi-modal representation of state changes.
**Action:** Always pair visual color changes with distinct, textual/emoji status markers to ensure interface accessibility.

## 2025-02-15 - Global Event Handling for Accessibility in CustomTkinter Utility Windows
**Learning:** For utility windows and live HUDs, keyboard accessibility (such as the Escape key to close the window) should be bound globally via `bind_all` rather than instance-level `bind`. Focus states can easily be captured by nested sub-widgets, preventing standard instance bindings from receiving keyboard events.
**Action:** Bind utility window dismissals globally using `bind_all("<Escape>", ...)` to guarantee reliable keyboard navigation.

## 2025-02-15 - Memory Leak and Teardown Prevention in CustomTkinter Schedules
**Learning:** Scheduling recurring updates using `.after()` in CustomTkinter/Tkinter can lead to orphaned event loops, memory leaks, and threading/Tcl errors on window teardown if the job continues running after widget destruction.
**Action:** Store the active schedule's job ID, override the `destroy()` method, and explicitly invoke `after_cancel()` to cleanly terminate scheduled loops on close.
