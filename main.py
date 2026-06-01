import sqlite3
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ---------------- IMPORT MODULE WINDOWS ----------------
from patients import open_patient_window
from doctors import open_doctor_window
from manage_records import open_record_management_window


# ---------------- DATABASE CONNECTION ENGINE ----------------
def get_db_connection():
    """Establish SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def get_table_count(table_name):
    """Safely fetch row counts from any specific table for live indicators."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    except Exception:
        return 0


def get_total_revenue():
    """Calculate aggregate medical collection for live performance statistics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_bill) FROM billing")
        total = cursor.fetchone()[0]
        conn.close()
        return f"Le {total:,.2f}" if total else "Le 0.00"
    except Exception:
        return "Le 0.00"


# ---------------- CONSULTATION WINDOW ----------------
def open_consultation_window():
    consult_win = Toplevel(root)
    consult_win.title("Consultation Desk")
    consult_win.geometry("900x650")
    consult_win.config(bg="#ECF0F1")
    consult_win.focus_set()

    symptoms_var = StringVar()
    diagnosis_var = StringVar()
    prescription_var = StringVar()
    revisit_var = StringVar()

    # ---------------- LOAD DATA UTILITIES ----------------
    def load_patients():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT patient_id, full_name FROM patients")
            records = cursor.fetchall()
        except sqlite3.Error:
            records = []
        finally:
            conn.close()
        return records

    def load_doctors():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT doctor_id, doctor_name FROM doctors")
            records = cursor.fetchall()
        except sqlite3.Error:
            records = []
        finally:
            conn.close()
        return records

    # ---------------- REFRESH FUNCTIONS ----------------
    def local_refresh_patients(*_):
        patient_combo["values"] = [f"{r[0]} - {r[1]}" for r in load_patients()]

    def local_refresh_doctors(*_):
        doctor_combo["values"] = [f"{r[0]} - {r[1]}" for r in load_doctors()]

    # ---------------- REVISIT DATE ENGINE ----------------
    def calculate_revisit(diag_text):
        norm = diag_text.lower()
        if "malaria" in norm:
            days_offset = 3
        elif "typhoid" in norm:
            days_offset = 7
        else:
            days_offset = 14
        return (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")

    # ---------------- SAVE CONSULTATION ----------------
    def process_consultation_save():
        if not patient_combo.get().strip():
            messagebox.showerror("Validation Error", "Please select a patient.")
            return

        if not doctor_combo.get().strip():
            messagebox.showerror("Validation Error", "Please select a doctor.")
            return

        try:
            p_id = patient_combo.get().split("-")[0].strip()
            d_id = doctor_combo.get().split("-")[0].strip()
            symptom_data = symptoms_var.get()
            diag_data = diagnosis_var.get()
            presc_data = prescription_var.get()

            revisit_date = calculate_revisit(diag_data)
            revisit_var.set(revisit_date)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO consultations (patient_id, doctor_id, symptoms, diagnosis, prescription, revisit_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (p_id, d_id, symptom_data, diag_data, presc_data, revisit_date)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Consultation Saved Successfully!\nRevisit Date: {revisit_date}")
            refresh_dashboard_metrics()  # Sync main metrics frame instantly
            consult_win.destroy()
        except Exception as error:
            messagebox.showerror("Engine Failure", f"Could not save consultation:\n{error}")

    # ---------------- UI LAYOUT ----------------
    Label(consult_win, text="CONSULTATION DESK", font=("Arial", 18, "bold"), bg="#2C3E50", fg="white").pack(fill=X)

    form_frame = Frame(consult_win, bg="#ECF0F1")
    form_frame.pack(pady=40)

    Label(form_frame, text="Patient", bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    patient_combo = ttk.Combobox(form_frame, width=40, state="readonly")
    patient_combo.grid(row=0, column=1, pady=10)
    patient_combo.bind("<Button-1>", local_refresh_patients)

    Label(form_frame, text="Doctor", bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    doctor_combo = ttk.Combobox(form_frame, width=40, state="readonly")
    doctor_combo.grid(row=1, column=1, pady=10)
    doctor_combo.bind("<Button-1>", local_refresh_doctors)

    local_refresh_patients()
    local_refresh_doctors()

    Label(form_frame, text="Symptoms", bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=symptoms_var, width=42).grid(row=2, column=1, pady=10)

    Label(form_frame, text="Diagnosis", bg="#ECF0F1").grid(row=3, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=diagnosis_var, width=42).grid(row=3, column=1, pady=10)

    Label(form_frame, text="Prescription", bg="#ECF0F1").grid(row=4, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=prescription_var, width=42).grid(row=4, column=1, pady=10)

    Button(consult_win, text="Save Consultation", bg="#2C3E50", fg="white", font=("Arial", 11, "bold"), padx=15, pady=8,
           command=process_consultation_save).pack(pady=20)


# ---------------- BILLING WINDOW ----------------
def open_billing_window():
    billing_win = Toplevel(root)
    billing_win.title("Billing Operations Desk")
    billing_win.geometry("800x600")
    billing_win.config(bg="#F8F9F9")
    billing_win.focus_set()

    consultation_var = DoubleVar(value=0.0)
    medicine_var = DoubleVar(value=0.0)
    treatment_var = DoubleVar(value=0.0)

    def load_patients_local():
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT patient_id, full_name FROM patients")
            records = cursor.fetchall()
        except sqlite3.Error:
            records = []
        finally:
            conn.close()
        return records

    def local_refresh_billing_patients(*_):
        billing_patient_combo["values"] = [f"{r[0]} - {r[1]}" for r in load_patients_local()]

    def commit_and_calculate_bill():
        if not billing_patient_combo.get().strip():
            messagebox.showerror("Validation Error", "Please select a patient.")
            return

        try:
            p_id = billing_patient_combo.get().split("-")[0].strip()
            c_fee = consultation_var.get()
            m_fee = medicine_var.get()
            t_fee = treatment_var.get()
            total_bill = c_fee + m_fee + t_fee

            result_label.config(text=f"Total Invoice Balance: Le {total_bill:,.2f}")

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO billing (patient_id, consultation_fee, medicine_fee, treatment_fee, total_bill)
                VALUES (?, ?, ?, ?, ?)
                """,
                (p_id, c_fee, m_fee, t_fee, total_bill)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Billing Saved Successfully.")
            refresh_dashboard_metrics()  # Sync metrics post financial tracking transaction
            billing_win.destroy()
        except Exception as error:
            messagebox.showerror("Billing Error", str(error))

    # ---------------- UI LAYOUT ----------------
    Label(billing_win, text="FINANCIAL BILLING PANEL", font=("Arial", 16, "bold"), bg="#0B1F3A", fg="white").pack(
        fill=X)

    b_frame = Frame(billing_win, bg="white", padx=20, pady=20)
    b_frame.pack(pady=35)

    Label(b_frame, text="Patient", bg="white").grid(row=0, column=0, pady=10, sticky=W)
    billing_patient_combo = ttk.Combobox(b_frame, width=32, state="readonly")
    billing_patient_combo.grid(row=0, column=1, pady=10)
    billing_patient_combo.bind("<Button-1>", local_refresh_billing_patients)
    local_refresh_billing_patients()

    Label(b_frame, text="Consultation Fee", bg="white").grid(row=1, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=consultation_var, width=35).grid(row=1, column=1, pady=10)

    Label(b_frame, text="Medicine Fee", bg="white").grid(row=2, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=medicine_var, width=35).grid(row=2, column=1, pady=10)

    Label(b_frame, text="Treatment Fee", bg="white").grid(row=3, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=treatment_var, width=35).grid(row=3, column=1, pady=10)

    Button(billing_win, text="Save Billing", bg="#0B1F3A", fg="white", width=30, height=2,
           command=commit_and_calculate_bill).pack(pady=15)

    result_label = Label(billing_win, text="", font=("Arial", 14, "bold"), bg="#F8F9F9", fg="green")
    result_label.pack(pady=10)


# ---------------- REPORT WINDOW ----------------
def open_reports_window():
    try:
        import reports
        # Trigger report sequence if built modularly
    except ModuleNotFoundError:
        messagebox.showerror("Error", "reports.py file could not be found.")


# ---------------- ENGINE TO REFRESH THE LIVE DASHBOARD STATS ----------------
def refresh_dashboard_metrics():
    """Queries structural counts dynamically to populate screen information panels."""
    lbl_stat_patients.config(text=str(get_table_count("patients")))
    lbl_stat_doctors.config(text=str(get_table_count("doctors")))
    lbl_stat_consults.config(text=str(get_table_count("consultations")))
    lbl_stat_rev.config(text=get_total_revenue())


# ---------------- MAIN APPLICATION SETUP ----------------
root = Tk()
root.title("Sierra Leone Community Health Management System")
root.geometry("1200x700")
root.config(bg="#0B1F3A")

# ---------------- TITLES ----------------
heading = Label(root, text="SIERRA LEONE COMMUNITY HEALTH MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#0B1F3A",
                fg="white")
heading.pack(pady=20)

welcome = Label(root, text="Welcome to the Digital Clinic Management Platform", font=("Arial", 14), bg="#0B1F3A",
                fg="lightgray")
welcome.pack(pady=5)

# ---------------- MAIN DASHBOARD PANEL CONTAINER ----------------
dashboard_container_frame = Frame(root, bg="#F2F4F4", width=1100, height=480, bd=2, relief=RIDGE)
dashboard_container_frame.pack(pady=15)
dashboard_container_frame.pack_propagate(False)

# ---- LEFT SIDE: MENU NAVIGATION SYSTEM PANELS ----
menu_frame = LabelFrame(dashboard_container_frame, text=" System Operations Menu ", font=("Arial", 11, "bold"),
                        bg="#F2F4F4", fg="#0B1F3A", padx=20, pady=20)
menu_frame.place(x=30, y=20, width=450, height=420)

btn_patient = Button(menu_frame, text="👤 Patient Registration", width=22, height=2, font=("Arial", 10),
                     command=open_patient_window)
btn_patient.grid(row=0, column=0, padx=15, pady=15)

btn_doctor = Button(menu_frame, text="🩺 Doctor Management", width=22, height=2, font=("Arial", 10),
                    command=open_doctor_window)
btn_doctor.grid(row=1, column=0, padx=15, pady=15)

btn_manage = Button(menu_frame, text="📂 Record Management", width=22, height=2, font=("Arial", 10),
                    command=open_record_management_window)
btn_manage.grid(row=0, column=1, padx=15, pady=15)

btn_consult = Button(menu_frame, text="📝 Consultation Desk", width=22, height=2, font=("Arial", 10),
                     command=open_consultation_window)
btn_consult.grid(row=1, column=1, padx=15, pady=15)

btn_billing = Button(menu_frame, text="💳 Billing Operations", width=22, height=2, font=("Arial", 10),
                     command=open_billing_window)
btn_billing.grid(row=2, column=0, padx=15, pady=15)

btn_reports = Button(menu_frame, text="📊 Reports & Analytics", width=22, height=2, font=("Arial", 10),
                     command=open_reports_window)
btn_reports.grid(row=2, column=1, padx=15, pady=15)

# ---- RIGHT SIDE: DASHBOARD STATISTICS & REPORT SUMMARY CARD BLOCKS ----
stats_frame = LabelFrame(dashboard_container_frame, text=" Live Facility Analytical Overview ",
                         font=("Arial", 11, "bold"), bg="#F2F4F4", fg="#0B1F3A", padx=20, pady=20)
stats_frame.place(x=520, y=20, width=540, height=420)

# Card 1: Patients Total
card1 = Frame(stats_frame, bg="#3498DB", bd=1, relief=SOLID)
card1.place(x=15, y=15, width=220, height=100)
Label(card1, text="TOTAL REGISTERED PATIENTS", font=("Arial", 9, "bold"), bg="#3498DB", fg="white").pack(pady=10)
lbl_stat_patients = Label(card1, text="0", font=("Arial", 22, "bold"), bg="#3498DB", fg="white")
lbl_stat_patients.pack()

# Card 2: Active Doctors
card2 = Frame(stats_frame, bg="#2ECC71", bd=1, relief=SOLID)
card2.place(x=265, y=15, width=220, height=100)
Label(card2, text="ACTIVE CLINICAL DOCTORS", font=("Arial", 9, "bold"), bg="#2ECC71", fg="white").pack(pady=10)
lbl_stat_doctors = Label(card2, text="0", font=("Arial", 22, "bold"), bg="#2ECC71", fg="white")
lbl_stat_doctors.pack()

# Card 3: Total Consultations Completed
card3 = Frame(stats_frame, bg="#E67E22", bd=1, relief=SOLID)
card3.place(x=15, y=140, width=220, height=100)
Label(card3, text="CONSULTATIONS LOGGED", font=("Arial", 9, "bold"), bg="#E67E22", fg="white").pack(pady=10)
lbl_stat_consults = Label(card3, text="0", font=("Arial", 22, "bold"), bg="#E67E22", fg="white")
lbl_stat_consults.pack()

# Card 4: Financial Collections Aggregate
card4 = Frame(stats_frame, bg="#9B59B6", bd=1, relief=SOLID)
card4.place(x=265, y=140, width=220, height=100)
Label(card4, text="TOTAL MEDICAL INVOICES", font=("Arial", 9, "bold"), bg="#9B59B6", fg="white").pack(pady=10)
lbl_stat_rev = Label(card4, text="Le 0.00", font=("Arial", 16, "bold"), bg="#9B59B6", fg="white")
lbl_stat_rev.pack(pady=5)

# Quick System Manual Checklist Label
Manual_label = Label(stats_frame,
                     text="💡 Quick Tip: Metrics update instantly whenever data is safely saved\nacross registration forms, consultation logs, or processing desks.",
                     font=("Arial", 9, "italic"), bg="#F2F4F4", fg="gray", justify=LEFT)
Manual_label.place(x=15, y=275)

# Refresh button to trigger updates on user demand
btn_refresh = Button(stats_frame, text="🔄 Recalculate Statistics", font=("Arial", 10, "bold"), bg="#0B1F3A", fg="white",
                     command=refresh_dashboard_metrics, cursor="hand2")
btn_refresh.place(x=15, y=320, width=470, height=35)

# ---------------- EXIT INFRASTRUCTURE ----------------
exit_btn = Button(root, text="Exit System Infrastructure", font=("Arial", 12, "bold"), bg="#C0392B", fg="white",
                  padx=10, command=root.destroy, cursor="hand2")
exit_btn.pack(pady=10)

# Initialize counts upon system launching
refresh_dashboard_metrics()

# ---------------- RUN INFRASTRUCTURE ENGINE ----------------
root.mainloop()