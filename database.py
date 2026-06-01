import sqlite3

# Connect Database
conn = sqlite3.connect("clinic.db")

# Create Cursor
cursor = conn.cursor()

# Enable Foreign Keys
cursor.execute("PRAGMA foreign_keys=ON")


# ------ PATIENT TABLE ------
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
    
    phone TEXT UNIQUE
)
''')


# ------ DOCTOR TABLE ------
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors(
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_code TEXT UNIQUE,
    doctor_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT UNIQUE,
    availability TEXT,

    UNIQUE(doctor_name,specialization)
)
''')


# ------ CONSULTATIONS TABLE ------
cursor.execute('''
CREATE TABLE IF NOT EXISTS consultations(
    consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    symptoms TEXT,
    diagnosis TEXT,
    prescription TEXT,
    revisit_date TEXT,

    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id),
    FOREIGN KEY(doctor_id)
    REFERENCES doctors(doctor_id)
)
''')


# ------ BILLING TABLE ------
cursor.execute('''
CREATE TABLE IF NOT EXISTS billing(
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    consultation_fee REAL,
    medicine_fee REAL,
    treatment_fee REAL,
    total_bill REAL,
    
    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)
)
''')


# ------USERS TABLE ------
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')


cursor.execute('''
INSERT OR IGNORE INTO users
(username,password,role)

VALUES
('alhajifodaykoroma','Emperordangotae@1997','Administrator')
''')


conn.commit()

conn.close()

print("Database created successfully")