## 2025-02-18 - Colorblind Accessibility & Memory Leak Prevention in CustomTkinter HUDs
**Learning:** For desktop utility HUDs and widgets in Tkinter or CustomTkinter:
- Combining color transitions with multi-modal visual indicators (such as distinct emojis like 🟢 and 🚨) satisfies WCAG 1.4.1 (Use of Color), helping colorblind users instantly perceive system state changes.
- Binding the `<Escape>` key globally via `bind_all` ensures a delightful and highly accessible keyboard shortcut to quickly close top-level utility HUDs, regardless of which widget currently has active keyboard focus.
- Overriding the `destroy` method to cancel any scheduled `.after()` event loops via `after_cancel()` avoids silent memory leaks and background threading/Tcl errors when the HUD window is closed.
**Action:** Always combine color cues with textual/emoji visual indicators for critical statuses, bind keyboard escape routes globally, and clean up scheduled callbacks upon widget destruction in Tkinter-based apps.
