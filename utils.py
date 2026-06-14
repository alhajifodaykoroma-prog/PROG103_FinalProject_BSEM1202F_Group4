    import sqlite3

# Generate Patient Code

def generate_patient_code():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(patient_id) FROM patients")
    res = cursor.fetchone()[0]
    next_id = (res if res else 0) + 1
    conn.close()
    return f"PAT{next_id:03d}"



# Generate Doctor Code

def generate_doctor_code():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(doctor_id) FROM doctors")
    res = cursor.fetchone()[0]
    next_id = (res if res else 0) + 1
    conn.close()
    return f"DOC{next_id:03d}"