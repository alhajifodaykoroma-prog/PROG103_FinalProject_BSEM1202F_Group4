"""
seed_mock_data.py
-----------------
Creates clinic.db (if missing) and loads realistic demo data for the
Sierra Leone Community Health Management System so the dashboard, record
management screens and reports display live numbers during a demo.

Safe to re-run: it clears the patients / doctors / consultations / billing
tables first, then re-seeds. The login user is preserved with INSERT OR IGNORE.
"""

import sqlite3

conn = sqlite3.connect("clinic.db")
conn.execute("PRAGMA foreign_keys=ON")
cursor = conn.cursor()

# ---------------- ENSURE SCHEMA (matches database.py) ----------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_code TEXT UNIQUE,
    full_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    address TEXT,
    symptoms TEXT,
    registration_date TEXT,
    status TEXT DEFAULT 'Active',
    phone TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors(
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_code TEXT UNIQUE,
    doctor_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT UNIQUE,
    availability TEXT,
    employment_status TEXT DEFAULT 'Active',
    UNIQUE(doctor_name,specialization)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS consultations(
    consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    symptoms TEXT,
    diagnosis TEXT,
    prescription TEXT,
    revisit_date TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS billing(
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    consultation_fee REAL,
    medicine_fee REAL,
    treatment_fee REAL,
    total_bill REAL,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# ---------------- LOGIN USER ----------------
cursor.execute(
    "INSERT OR IGNORE INTO users (username,password,role) VALUES (?,?,?)",
    ("robertissackamara", "Do3tors@veslives", "Administrator")
)


# ---------------- RESET DEMO TABLES (idempotent re-seed) ----------------
for tbl in ("billing", "consultations", "doctors", "patients"):
    cursor.execute(f"DELETE FROM {tbl}")
cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name IN ('patients','doctors','consultations','billing')"
)

# ---------------- DOCTORS ----------------
doctors = [
    ("DOC001", "Dr. Aminata Sesay",   "General Doctor", "+23276123456", "08:00 - 16:00", "Active"),
    ("DOC002", "Dr. Mohamed Kamara",  "Pediatrician",   "+23277234567", "09:00 - 17:00", "Active"),
    ("DOC003", "Dr. Fatmata Bangura", "Cardiologist",   "+23278345678", "08:00 - 14:00", "Active"),
    ("DOC004", "Dr. Ibrahim Conteh",  "Surgeon",        "+23279456789", "10:00 - 18:00", "Active"),
    ("DOC005", "Dr. Isata Koroma",    "Dentist",        "+23288567890", "08:00 - 15:00", "Retired"),
]
cursor.executemany(
    "INSERT INTO doctors (doctor_code,doctor_name,specialization,phone,availability,employment_status) "
    "VALUES (?,?,?,?,?,?)",
    doctors
)

# ---------------- PATIENTS ----------------
patients = [
    ("PAT001", "Aminata Turay",   28, "Female", "+23276000001", "Brookfields, Freetown", "Fever and chills",      "2026-05-20", "Active"),
    ("PAT002", "Mohamed Bangura", 45, "Male",   "+23276000002", "Kissy, Freetown",       "Headache and fatigue",  "2026-05-22", "Active"),
    ("PAT003", "Hawa Sesay",       6, "Female", "+23276000003", "Wellington, Freetown",  "High fever",            "2026-05-24", "Active"),
    ("PAT004", "Abu Kamara",      34, "Male",   "+23276000004", "Aberdeen, Freetown",    "Abdominal pain",        "2026-05-25", "Active"),
    ("PAT005", "Fatmata Koroma",  52, "Female", "+23276000005", "Lumley, Freetown",      "Chest pain",            "2026-05-27", "Active"),
    ("PAT006", "Ibrahim Jalloh",  19, "Male",   "+23276000006", "Congo Cross, Freetown", "Persistent cough",      "2026-05-28", "Active"),
    ("PAT007", "Mariama Conteh",  30, "Female", "+23276000007", "Murray Town, Freetown", "Toothache",             "2026-05-29", "Active"),
    ("PAT008", "Sorie Mansaray",  60, "Male",   "+23276000008", "Calaba Town, Freetown", "Joint pain",            "2026-05-30", "Discharged"),
    ("PAT009", "Kadiatu Bah",     24, "Female", "+23276000009", "Goderich, Freetown",    "Nausea and vomiting",   "2026-06-01", "Active"),
    ("PAT010", "Alusine Fofanah", 41, "Male",   "+23276000010", "Hill Station, Freetown","Lower back pain",       "2026-06-03", "Active"),
    ("PAT011", "Isatu Dumbuya",    8, "Female", "+23276000011", "Waterloo, Freetown",    "Malaria symptoms",      "2026-06-05", "Active"),
    ("PAT012", "Santigie Kargbo", 37, "Male",   "+23276000012", "Tower Hill, Freetown",  "Typhoid symptoms",      "2026-06-07", "Active"),
]
cursor.executemany(
    "INSERT INTO patients (patient_code,full_name,age,gender,phone,address,symptoms,registration_date,status) "
    "VALUES (?,?,?,?,?,?,?,?,?)",
    patients
)


# ---------------- CONSULTATIONS ----------------
# (patient_id, doctor_id, symptoms, diagnosis, prescription, revisit_date)
consultations = [
    (1,  1, "Fever and chills",     "Malaria",       "ACT + Paracetamol",        "2026-06-09"),
    (3,  2, "High fever",           "Malaria",       "Pediatric ACT syrup",      "2026-06-12"),
    (5,  3, "Chest pain",           "Hypertension",  "Amlodipine 5mg daily",     "2026-06-20"),
    (4,  4, "Abdominal pain",       "Appendicitis",  "Surgical referral",        "2026-06-14"),
    (7,  5, "Toothache",            "Dental caries", "Extraction + analgesics",  "2026-06-22"),
    (12, 1, "Typhoid symptoms",     "Typhoid",       "Ciprofloxacin 500mg",      "2026-06-15"),
    (11, 2, "Malaria symptoms",     "Malaria",       "ACT course",               "2026-06-10"),
    (2,  1, "Headache and fatigue", "Malaria",       "ACT + rehydration salts",  "2026-06-11"),
]
cursor.executemany(
    "INSERT INTO consultations (patient_id,doctor_id,symptoms,diagnosis,prescription,revisit_date) "
    "VALUES (?,?,?,?,?,?)",
    consultations
)

# ---------------- BILLING ----------------
# (patient_id, consultation_fee, medicine_fee, treatment_fee, total_bill)
billing = [
    (1,  50.0, 120.0,   0.0, 170.0),
    (3,  30.0,  90.0,   0.0, 120.0),
    (5,  80.0, 150.0, 200.0, 430.0),
    (4,  60.0, 100.0, 500.0, 660.0),
    (7,  40.0,  60.0, 300.0, 400.0),
    (12, 50.0, 200.0,   0.0, 250.0),
    (11, 30.0,  90.0,   0.0, 120.0),
    (2,  50.0, 110.0,   0.0, 160.0),
]
cursor.executemany(
    "INSERT INTO billing (patient_id,consultation_fee,medicine_fee,treatment_fee,total_bill) "
    "VALUES (?,?,?,?,?)",
    billing
)

conn.commit()

# ---------------- SUMMARY ----------------
def _count(t):
    return cursor.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]

rev = cursor.execute("SELECT SUM(total_bill) FROM billing").fetchone()[0] or 0
print("Mock data seeded successfully.")
print(f"  Patients      : {_count('patients')}")
print(f"  Doctors       : {_count('doctors')}")
print(f"  Consultations : {_count('consultations')}")
print(f"  Bills         : {_count('billing')}")
print(f"  Total revenue : Le {rev:,.2f}")
print("  Login         : robertissackamara / Do3tors@veslives")

conn.close()
