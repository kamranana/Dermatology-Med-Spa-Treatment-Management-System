# view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from bll import MedSpaService

# Advanced feature: charting
import matplotlib.pyplot as plt


class LoginWindow(tk.Frame):
    """Login / connection info screen."""

    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success

        self.host_var = tk.StringVar(value="localhost")
        self.port_var = tk.StringVar(value="3306")
        self.user_var = tk.StringVar(value="root")
        self.password_var = tk.StringVar()
        self.db_name_var = tk.StringVar(value="derm_medspa")

        tk.Label(self, text="Database Login", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Host:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.host_var).grid(row=1, column=1)

        tk.Label(self, text="Port:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.port_var).grid(row=2, column=1)

        tk.Label(self, text="User:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.user_var).grid(row=3, column=1)

        tk.Label(self, text="Password:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=4, column=1)

        tk.Label(self, text="Database:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.db_name_var).grid(row=5, column=1)

        tk.Button(self, text="Connect", command=self.connect).grid(row=6, column=0, columnspan=2, pady=10)

        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.grid(row=7, column=0, columnspan=2)

    def connect(self):
        host = self.host_var.get()
        port = int(self.port_var.get())
        user = self.user_var.get()
        password = self.password_var.get()
        db_name = self.db_name_var.get()

        try:
            self.on_login_success(host, port, user, password, db_name)
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {e}")


class MainWindow(tk.Frame):
    """Main GUI window after successful login."""

    def __init__(self, master, service: MedSpaService):
        super().__init__(master)
        self.service = service

        tk.Label(self, text="Dermatology & Med Spa Management",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Patient list
        self.tree = ttk.Treeview(self, columns=("id", "name", "phone", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Refresh Patients", command=self.refresh_patients).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add Patient", command=self.add_patient_dialog).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_patient_dialog).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_patient).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Show Revenue Chart (Advanced)", command=self.show_revenue_chart).grid(row=0, column=4, padx=5)

        self.status_label = tk.Label(self, text="", fg="blue")
        self.status_label.pack(pady=5)

        self.refresh_patients()

    def refresh_patients(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            patients = self.service.list_patients()
            for p in patients:
                name = f"{p['first_name']} {p['last_name']}"
                self.tree.insert("", "end", values=(p['patient_id'], name, p['phone'], p['email']))
            self.status_label.config(text=f"Loaded {len(patients)} patients.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
            self.status_label.config(text="Error loading patients.")

    def add_patient_dialog(self):
        try:
            first = simpledialog.askstring("Add Patient", "First name:")
            if not first:
                return
            last = simpledialog.askstring("Add Patient", "Last name:")
            if not last:
                return
            dob_str = simpledialog.askstring("Add Patient", "Date of birth (YYYY-MM-DD, optional):")
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
            phone = simpledialog.askstring("Add Patient", "Phone:")
            email = simpledialog.askstring("Add Patient", "Email:")
            gender = "Female"   # could be improved with a dropdown
            skin_type = "Combination"
            self.service.create_patient(first, last, dob, gender, phone, email,
                                        skin_type, 1, 1)
            self.status_label.config(text="Patient added.")
            self.refresh_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {e}")
            self.status_label.config(text="Error adding patient.")

    def get_selected_patient_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a patient.")
            return None
        values = self.tree.item(selected[0], "values")
        return int(values[0])

    def edit_patient_dialog(self):
        pid = self.get_selected_patient_id()
        if pid is None:
            return
        try:
            first = simpledialog.askstring("Edit Patient", "New first name:")
            last = simpledialog.askstring("Edit Patient", "New last name:")
            if not first or not last:
                return
            # For simplicity, we only change names & mark patient active.
            self.service.edit_patient(
                pid, first, last, None, "Female", "", "", "Combination", 1, 1, 1
            )
            self.status_label.config(text="Patient updated.")
            self.refresh_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {e}")
            self.status_label.config(text="Error updating patient.")

    def delete_patient(self):
        pid = self.get_selected_patient_id()
        if pid is None:
            return
        if not messagebox.askyesno("Confirm", "Delete this patient and related data?"):
            return
        try:
            self.service.remove_patient(pid)
            self.status_label.config(text="Patient deleted.")
            self.refresh_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete patient: {e}")
            self.status_label.config(text="Error deleting patient.")

    def show_revenue_chart(self):
        try:
            data = self.service.get_revenue_by_category()
            categories = [row["category"] for row in data]
            revenue = [float(row["total_revenue"]) for row in data]

            if not categories:
                messagebox.showinfo("No Data", "No revenue data available.")
                return

            plt.figure()
            plt.bar(categories, revenue)
            plt.title("Revenue by Service Category")
            plt.xlabel("Category")
            plt.ylabel("Total Revenue ($)")
            plt.tight_layout()
            plt.show()
            self.status_label.config(text="Displayed revenue chart.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load chart data: {e}")
            self.status_label.config(text="Error displaying chart.")
