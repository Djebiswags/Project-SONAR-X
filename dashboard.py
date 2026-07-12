import psutil
import sys


def _import_customtkinter():
    try:
        import customtkinter as ctk
        return ctk
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "customtkinter (and its Tkinter dependencies) are required to run the HUD. "
            "Install Tkinter and customtkinter, or run the app without the HUD."
        ) from exc


def create_dashboard():
    ctk = _import_customtkinter()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    class SonarHUD(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("SONAR-X | Live Telemetry")
            self.geometry("350x220")
            self.attributes("-topmost", True)

            # Bind Escape key to close the HUD for seamless keyboard accessibility
            self.bind("<Escape>", lambda event: self.destroy())

            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.cpu_label = ctk.CTkLabel(
                self,
                text="🟢 CPU Load: --%",
                font=("Helvetica", 24, "bold"),
                text_color="#00FFCC",
            )
            self.cpu_label.grid(row=0, column=0, pady=(15, 10))

            self.ram_label = ctk.CTkLabel(
                self,
                text="🟢 RAM Usage: --%",
                font=("Helvetica", 18),
                text_color="#DCE4EE"
            )
            self.ram_label.grid(row=1, column=0, pady=10)

            # Keyboard accessibility hint
            self.esc_label = ctk.CTkLabel(
                self,
                text="Press ESC to exit",
                font=("Helvetica", 11, "italic"),
                text_color="#777777"
            )
            self.esc_label.grid(row=2, column=0, pady=(5, 15))

            self.update_telemetry()

        def update_telemetry(self):
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            # Multi-modal color and icon indicators for high resource usage (WCAG 1.4.1)
            cpu_color = "#FF3333" if cpu > 80 else "#00FFCC"
            cpu_emoji = "🚨" if cpu > 80 else "🟢"

            ram_color = "#FF3333" if ram > 80 else "#DCE4EE"
            ram_emoji = "🚨" if ram > 80 else "🟢"

            self.cpu_label.configure(text=f"{cpu_emoji} CPU Load: {cpu}%", text_color=cpu_color)
            self.ram_label.configure(text=f"{ram_emoji} RAM Usage: {ram}%", text_color=ram_color)
            self.after(1500, self.update_telemetry)

    return SonarHUD()


def main() -> None:
    hud = create_dashboard()
    hud.mainloop()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
