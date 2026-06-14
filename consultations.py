import sqlite3
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
CARD_BG   = "#FFFFFF"
TEXT_DARK = "#0F2440"
FONT      = "Lato"


def _hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


# ---------------- Database Connection ----------------
def get_connection():
    """Establishes a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------- Dropdown Auto-Refresh Functions ----------------
def refresh_patient_dropdown(*_):
    """Refreshes patient dropdown list dynamically.

    Note: '*_' absorbs the Tkinter event argument to prevent PyCharm linting
    warnings.
    """
    fresh_patients = load_patients()
    patient_combo["values"] = [f"{row[0]} - {row[1]}" for row in fresh_patients]


def refresh_doctor_dropdown(*_):
    """Refreshes doctor dropdown list dynamically."""
    fresh_doctors = load_doctors()
    doctor_combo["values"] = [f"{row[0]} - {row[1]}" for row in fresh_doctors]


# ---------------- Doctor Allocation Helper ----------------
def allocate_doctor(symptom):
    """Suggests a doctor specialty based on matching keywords in symptoms."""
    symptom_lower = symptom.lower()
    if "tooth" in symptom_lower:
        return "Dentist"
    elif "heart" in symptom_lower:
        return "Cardiologist"
    elif "child" in symptom_lower:
        return "Pediatrician"
    else:
        return "General Doctor"


# ---------------- Revisit Recommendation ----------------
def recommend_revisit(diagnosis):
    """Calculates a recommended revisit date based on medical diagnosis."""
    diagnosis_lower = diagnosis.lower()
    if "malaria" in diagnosis_lower:
        return (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    elif "typhoid" in diagnosis_lower:
        return (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        return (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")


# ---------------- Database Data Fetching ----------------
def load_patients():
    """Fetches unique records from the patients table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT patient_id, full_name FROM patients")
        data = cursor.fetchall()
    except sqlite3.Error:
        data = []
    finally:
        conn.close()
    return data


# ---------------- Load Doctors ----------------
def load_doctors():
    """Fetches unique records from the doctors table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT doctor_id, doctor_name FROM doctors")
        data = cursor.fetchall()
    except sqlite3.Error:
        data = []
    finally:
        conn.close()
    return data


# ---------------- Save Action Execution ----------------
def save_consultation():
    """Validates inputs and commits the transaction into the consultations table."""
    if not patient_combo.get().strip():
        messagebox.showerror("Error", "Select patient")
        return

    if not doctor_combo.get().strip():
        messagebox.showerror("Error", "Select doctor")
        return

    try:
        # Extract ID safely from UI format "ID - Name"
        patient_id = patient_combo.get().split("-")[0].strip()
        doctor_id = doctor_combo.get().split("-")[0].strip()

        symptoms = symptoms_var.get()
        diagnosis = diagnosis_var.get()
        prescription = prescription_var.get()

        revisit = recommend_revisit(diagnosis)
        revisit_var.set(revisit)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO consultations (patient_id, doctor_id, symptoms, diagnosis, prescription, revisit_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_id, doctor_id, symptoms, diagnosis, prescription, revisit),
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success", f"Consultation saved\nRecommended Revisit: {revisit}"
        )

    except Exception as err:
        messagebox.showerror("System Error", str(err))


# ---------------- UI Window Architecture ----------------
root = Tk()
root.title("Consultation System")
root.geometry("900x650")
root.config(bg="#ECF0F1")
root.option_add("*Font", (FONT, 10))
root.option_add("*Entry.relief", "solid")
root.option_add("*Entry.borderWidth", "1")

# ---------------- TTK CLINICAL STYLING ----------------
_style = ttk.Style(root)
try:
    _style.theme_use("clam")
except Exception:
    pass
_style.configure("TCombobox", font=(FONT, 10), padding=4)

# Tkinter Form Global Tracker Variables
patient_var = StringVar()
doctor_var = StringVar()
symptoms_var = StringVar()
diagnosis_var = StringVar()
prescription_var = StringVar()
revisit_var = StringVar()

# Header Element Top-level banner
Label(
    root,
    text="Consultation Management",
    font=(FONT, 20, "bold"),
    bg=NAVY,
    fg="white",
    pady=16,
).pack(fill=X)

# Centralized Grid Form Layout Frame
frame = Frame(root, bg="#ECF0F1")
frame.pack(pady=30)

# Patient Row Form Field
Label(frame, text="Patient", bg="#ECF0F1").grid(
    row=0, column=0, padx=10, pady=10
)
patient_combo = ttk.Combobox(frame, width=40)
patient_combo.grid(row=0, column=1)

# Doctor Row Form Field
Label(frame, text="Doctor", bg="#ECF0F1").grid(
    row=1, column=0, padx=10, pady=10
)
doctor_combo = ttk.Combobox(frame, width=40)
doctor_combo.grid(row=1, column=1)

# Seed UI drop-downs during runtime initialization
initial_patients = load_patients()
patient_combo["values"] = [f"{row[0]} - {row[1]}" for row in initial_patients]

initial_doctors = load_doctors()
doctor_combo["values"] = [f"{row[0]} - {row[1]}" for row in initial_doctors]

# Dynamic UI interaction binds
patient_combo.bind("<Button-1>", refresh_patient_dropdown)
doctor_combo.bind("<Button-1>", refresh_doctor_dropdown)

# Symptoms Row Entry Field
Label(frame, text="Symptoms", bg="#ECF0F1").grid(
    row=2, column=0, padx=10, pady=10
)
Entry(frame, textvariable=symptoms_var, width=42).grid(row=2, column=1)

# Diagnosis Row Entry Field
Label(frame, text="Diagnosis", bg="#ECF0F1").grid(
    row=3, column=0, padx=10, pady=10
)
Entry(frame, textvariable=diagnosis_var, width=42).grid(row=3, column=1)

# Prescription Row Entry Field
Label(frame, text="Prescription", bg="#ECF0F1").grid(
    row=4, column=0, padx=10, pady=10
)
Entry(frame, textvariable=prescription_var, width=42).grid(row=4, column=1)

# Interactive Action Buttons
save_consultation_btn = Button(
    root,
    text="Save Consultation",
    bg=TEAL,
    fg="white",
    bd=0,
    cursor="hand2",
    activebackground=TEAL_DK,
    activeforeground="white",
    font=(FONT, 12, "bold"),
    padx=15,
    pady=8,
    command=save_consultation,
)
save_consultation_btn.pack(pady=20)
_hover(save_consultation_btn, TEAL, TEAL_DK)

root.mainloop()