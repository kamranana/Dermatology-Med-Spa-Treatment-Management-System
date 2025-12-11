# dal.py
import mysql.connector


class DatabaseAccess:
    """Data Access Layer: the ONLY place that talks directly to MySQL."""

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, host, port, user, password, database="derm_medspa"):
        self.conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # ---- PATIENTS ----

    def get_all_patients(self):
        self.cursor.callproc("sp_get_all_patients")
        for result in self.cursor.stored_results():
            return result.fetchall()
        return []

    def add_patient(self, first_name, last_name, dob, gender, phone,
                    email, skin_type, is_new_patient, consent_on_file):
        args = (first_name, last_name, dob, gender, phone,
                email, skin_type, is_new_patient, consent_on_file)
        self.cursor.callproc("sp_add_patient", args)
        self.conn.commit()

    def update_patient(self, patient_id, first_name, last_name, dob, gender,
                       phone, email, skin_type, is_new_patient,
                       consent_on_file, is_active):
        args = (patient_id, first_name, last_name, dob, gender,
                phone, email, skin_type, is_new_patient,
                consent_on_file, is_active)
        self.cursor.callproc("sp_update_patient", args)
        self.conn.commit()

    def delete_patient(self, patient_id):
        self.cursor.callproc("sp_delete_patient_hard", (patient_id,))
        self.conn.commit()

    # ---- ANALYTICS (Advanced Feature) ----

    def get_revenue_by_category(self):
        self.cursor.callproc("sp_get_revenue_by_category")
        for result in self.cursor.stored_results():
            return result.fetchall()
        return []
