## 2025-05-18 - Safe Telemetry Update Scheduling in CustomTkinter
**Learning:** Calling `update_telemetry()` directly or re-triggering recurring `.after()` scheduling without first canceling any existing `_update_job` ID overwrites the reference, leaving orphaned Tcl timer callbacks that execute after window destruction and cause `invalid command name` Tcl errors.
**Action:** Always check and cancel `self._update_job` with `after_cancel()` at the start of recurring update methods as well as inside overridden `destroy()`.
