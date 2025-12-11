# Dermatology & Med Spa Treatment Management System

## Overview

This application is a dermatology and medical spa treatment management system designed for clinics that offer laser treatments, facials, acne treatments, microneedling sessions, chemical peels, and other cosmetic dermatology procedures.

Clinic staff can:

- Add, update, and delete patient records
- View patient lists
- (Extend) Manage appointments and treatment lines
- View summarized analytics and charts based on database views and stored procedures

The app is built using a 3-layer architecture (View, Business Logic, Data Access) and a MySQL database.

---

## How to Run the Application

### 1. Requirements

- Python 3.x
- MySQL server
- Python packages (install via pip):

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

1. Open MySQL Workbench or your SQL client.
2. Run the scripts in this order from the `db/` folder:

   - `01_schema_derm_medspa.sql`
   - `02_data_derm_medspa.sql`
   - `03_views_procedures_derm_medspa.sql`

This will create the `derm_medspa` database, tables, sample data, views, and stored procedures.

### 3. Run the Application

From the `derm_medspa_app/` folder:

```bash
python main.py
```

### 4. Log In Screen (Connection Information)

Before any data is shown, a **log-in window** is displayed.

- Host: default `localhost` (changeable)
- Port: default `3306` (changeable)
- User: your MySQL username (e.g., `root`)
- Password: your MySQL password
- Database: default `derm_medspa`

Click **Connect**. If login fails, an error message is displayed in red at the bottom of the login form.

---

## How the Application Meets the Requirements

1. **Submitted in a zip file**  
   - The whole project is contained in the `derm_medspa_app/` folder, which can be zipped and submitted.

2. **Readme with detailed instructions and advanced feature**  
   - This README explains how to run the app and documents the advanced feature:  
     > Displaying a bar chart of revenue by treatment category using `v_revenue_by_category` and `sp_get_revenue_by_category`.

3. **At least three distinct modules that separate view, business logic, data access layers**  
   - `view.py` – View layer (GUI)  
   - `bll.py` – Business Logic layer  
   - `dal.py` – Data Access layer

4. **Only the data access layer communicates with the database**  
   - All DB calls are in `dal.py` using `mysql.connector`.  
   - `view.py` uses `MedSpaService` from `bll.py`; `bll.py` uses `DatabaseAccess` from `dal.py`.

5. **Database connection info not hard-coded (except database name)**  
   - Host, port, user, and password are entered by the user on the login screen in `view.py`.  
   - A default database name `derm_medspa` is used but can be changed if needed.

6. **The data access layer only uses predefined stored procedures, functions, and views**  
   - `dal.py` calls stored procedures such as `sp_get_all_patients`, `sp_add_patient`, `sp_update_patient`, `sp_delete_patient_hard`, and `sp_get_revenue_by_category`.

7. **GUI view layer that is easy to read and understand**  
   - Implemented in `view.py` using Tkinter:  
     - Login screen  
     - Main window with patient list (Treeview), buttons for add/update/delete, and an advanced feature button for charts.

8. **View layer provides user feedback on actions/errors**  
   - Success and error messages are shown in a status label and via popup dialogs (`messagebox.showerror`, `messagebox.showwarning`, `messagebox.showinfo`).

9. **Login interface that precedes presentation of data**  
   - `main.py` shows `LoginWindow` first; only on successful connection does it show the `MainWindow`.

10. **Ability to add new information to at least one table**  
   - The **Add Patient** dialog in `MainWindow` calls `MedSpaService.create_patient`, which uses `sp_add_patient` to insert into `Patients`.

11. **Ability to update existing rows in at least one table**  
   - The **Edit Selected** button updates a patient’s information via `MedSpaService.edit_patient` and `sp_update_patient`.

12. **Ability to delete rows in at least one table**  
   - The **Delete Selected** button removes a patient via `MedSpaService.remove_patient` and `sp_delete_patient_hard`.  
   - Cascades to Appointments and Appointment_Treatments due to foreign key constraints.

13. **Ability to retrieve and view the data in the database**  
   - The patient list uses `sp_get_all_patients` → `v_patients_basic` to display data in a Treeview.

14. **Any information that changes in the tables should be reflected in the views**  
   - Stored procedures (insert/update/delete) change the underlying tables; views like `v_patients_basic` and `v_revenue_by_category` automatically reflect those changes.

15. **Advanced feature (not part of MRC project)**  
   - Advanced feature: **Revenue Chart by Category**  
     - View: `v_revenue_by_category`  
     - Procedure: `sp_get_revenue_by_category`  
     - GUI: **Show Revenue Chart (Advanced)** button in `MainWindow`  
     - Implementation: uses matplotlib to show a bar chart.  

16. **Application must run without crashing**  
   - Try/except blocks in the view layer catch errors and show user-friendly messages.  
   - Any unhandled exceptions can be wrapped further as needed.
