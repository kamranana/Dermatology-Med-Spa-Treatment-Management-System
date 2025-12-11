# bll.py
from dal import DatabaseAccess


class MedSpaService:
    """Business Logic Layer: enforces rules and orchestrates DAL calls."""

    def __init__(self):
        self.db = DatabaseAccess()

    # connection
    def connect(self, host, port, user, password, db_name="derm_medspa"):
        self.db.connect(host=host, port=port, user=user,
                        password=password, database=db_name)

    def close(self):
        self.db.close()

    # Patients
    def list_patients(self):
        return self.db.get_all_patients()

    def create_patient(self, first_name, last_name, dob, gender, phone,
                       email, skin_type, is_new_patient, consent_on_file):
        # Simple validation
        if not first_name or not last_name:
            raise ValueError("First and last name are required.")
        self.db.add_patient(first_name, last_name, dob, gender, phone,
                            email, skin_type, is_new_patient, consent_on_file)

    def edit_patient(self, patient_id, first_name, last_name, dob, gender,
                     phone, email, skin_type, is_new_patient,
                     consent_on_file, is_active):
        if not patient_id:
            raise ValueError("Patient ID is required.")
        self.db.update_patient(patient_id, first_name, last_name, dob, gender,
                               phone, email, skin_type, is_new_patient,
                               consent_on_file, is_active)

    def remove_patient(self, patient_id):
        self.db.delete_patient(patient_id)

    # Analytics
    def get_revenue_by_category(self):
        return self.db.get_revenue_by_category()
