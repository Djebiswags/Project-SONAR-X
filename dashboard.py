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
            self.geometry("350x200")
            self.attributes("-topmost", True)

            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.cpu_label = ctk.CTkLabel(
                self,
                text="CPU Load: --%",
                font=("Helvetica", 24, "bold"),
                text_color="#00FFCC",
            )
            self.cpu_label.grid(row=0, column=0, pady=20)

            self.ram_label = ctk.CTkLabel(self, text="RAM Usage: --%", font=("Helvetica", 18))
            self.ram_label.grid(row=1, column=0, pady=10)

            self.update_telemetry()

        def update_telemetry(self):
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            cpu_color = "#FF3333" if cpu > 80 else "#00FFCC"

            self.cpu_label.configure(text=f"CPU Load: {cpu}%", text_color=cpu_color)
            self.ram_label.configure(text=f"RAM Usage: {ram}%")
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
