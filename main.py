# main.py
import tkinter as tk
from bll import MedSpaService
from view import LoginWindow, MainWindow


def main():
    service = MedSpaService()

    root = tk.Tk()
    root.title("Dermatology & Med Spa Management")

    def on_login(host, port, user, password, db_name):
        # Called from LoginWindow
        service.connect(host, port, user, password, db_name)
        # If no exception, swap to main window
        login_frame.destroy()
        main_frame = MainWindow(root, service)
        main_frame.pack(fill="both", expand=True)

    login_frame = LoginWindow(root, on_login_success=on_login)
    login_frame.pack(fill="both", expand=True)

    root.mainloop()
    service.close()


if __name__ == "__main__":
    main()
