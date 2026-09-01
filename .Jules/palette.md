## 2026-07-22 - Multi-Modal Indicators & Global Key Bindings in CustomTkinter
**Learning:** Color-only status changes fail WCAG 1.4.1 for colorblind users; pairing color with visual indicators (e.g. 🟢/🚨) provides instant multi-modal feedback. Additionally, global shortcuts like `<Escape>` in Tkinter must be bound with `bind_all` to handle any widget focus state.
**Action:** Always combine color changes with icon/text indicators, bind window-level shortcuts with `bind_all`, and cancel `.after()` scheduled jobs on `destroy()`.
