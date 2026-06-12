import sqlite3
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ---------------- IMPORT MODULE WINDOWS ----------------
from patients import open_patient_window
from doctors import open_doctor_window
from manage_records import open_record_management_window

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
ACCENT    = "#14B8A6"
APP_BG    = "#EEF3F8"
CARD_BG   = "#FFFFFF"
PANEL_BG  = "#F8FAFC"
BORDER    = "#D7E0EC"
TEXT_DARK = "#0F2440"
TEXT_MUTE = "#64748B"
DANGER    = "#D7443E"
C_BLUE    = "#2563EB"
C_TEAL    = "#0EA5A4"
C_AMBER   = "#E08A1E"
C_VIOLET  = "#7C5CD6"
FONT      = "Lato"


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_horizontal_gradient(canvas, width, height, color_left, color_right):
    r1, g1, b1 = _hex_to_rgb(color_left)
    r2, g2, b2 = _hex_to_rgb(color_right)
    steps = max(width, 1)
    for i in range(steps):
        ratio = i / steps
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        canvas.create_line(i, 0, i, height, fill=f"#{r:02x}{g:02x}{b:02x}")


def _hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


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
    consult_win.config(bg=APP_BG)
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
    Label(consult_win, text="CONSULTATION DESK", font=(FONT, 17, "bold"), bg=NAVY, fg="white",
          pady=16).pack(fill=X)

    form_frame = Frame(consult_win, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1,
                       padx=30, pady=30)
    form_frame.pack(pady=40)

    Label(form_frame, text="Patient", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=0, column=0, padx=10, pady=10, sticky=W)
    patient_combo = ttk.Combobox(form_frame, width=40, state="readonly")
    patient_combo.grid(row=0, column=1, pady=10)
    patient_combo.bind("<Button-1>", local_refresh_patients)

    Label(form_frame, text="Doctor", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=1, column=0, padx=10, pady=10, sticky=W)
    doctor_combo = ttk.Combobox(form_frame, width=40, state="readonly")
    doctor_combo.grid(row=1, column=1, pady=10)
    doctor_combo.bind("<Button-1>", local_refresh_doctors)

    local_refresh_patients()
    local_refresh_doctors()

    Label(form_frame, text="Symptoms", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=2, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=symptoms_var, width=42, font=(FONT, 11),
          relief="solid", bd=1).grid(row=2, column=1, pady=10, ipady=4)

    Label(form_frame, text="Diagnosis", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=3, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=diagnosis_var, width=42, font=(FONT, 11),
          relief="solid", bd=1).grid(row=3, column=1, pady=10, ipady=4)

    Label(form_frame, text="Prescription", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=4, column=0, padx=10, pady=10, sticky=W)
    Entry(form_frame, textvariable=prescription_var, width=42, font=(FONT, 11),
          relief="solid", bd=1).grid(row=4, column=1, pady=10, ipady=4)

    save_consult_btn = Button(consult_win, text="Save Consultation", bg=TEAL, fg="white",
                              font=(FONT, 11, "bold"), padx=15, pady=9, bd=0, cursor="hand2",
                              activebackground=TEAL_DK, activeforeground="white",
                              command=process_consultation_save)
    save_consult_btn.pack(pady=20)
    _hover(save_consult_btn, TEAL, TEAL_DK)


# ---------------- BILLING WINDOW ----------------
def open_billing_window():
    billing_win = Toplevel(root)
    billing_win.title("Billing Operations Desk")
    billing_win.geometry("800x600")
    billing_win.config(bg=APP_BG)
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
    Label(billing_win, text="FINANCIAL BILLING PANEL", font=(FONT, 16, "bold"), bg=NAVY, fg="white",
          pady=16).pack(fill=X)

    b_frame = Frame(billing_win, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1,
                    padx=24, pady=24)
    b_frame.pack(pady=35)

    Label(b_frame, text="Patient", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=0, column=0, pady=10, sticky=W)
    billing_patient_combo = ttk.Combobox(b_frame, width=32, state="readonly")
    billing_patient_combo.grid(row=0, column=1, pady=10, padx=(12, 0))
    billing_patient_combo.bind("<Button-1>", local_refresh_billing_patients)
    local_refresh_billing_patients()

    Label(b_frame, text="Consultation Fee", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=1, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=consultation_var, width=35, font=(FONT, 11), relief="solid", bd=1).grid(
        row=1, column=1, pady=10, padx=(12, 0), ipady=4)

    Label(b_frame, text="Medicine Fee", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=2, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=medicine_var, width=35, font=(FONT, 11), relief="solid", bd=1).grid(
        row=2, column=1, pady=10, padx=(12, 0), ipady=4)

    Label(b_frame, text="Treatment Fee", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).grid(
        row=3, column=0, pady=10, sticky=W)
    Entry(b_frame, textvariable=treatment_var, width=35, font=(FONT, 11), relief="solid", bd=1).grid(
        row=3, column=1, pady=10, padx=(12, 0), ipady=4)

    save_billing_btn = Button(billing_win, text="Save Billing", bg=TEAL, fg="white", width=30, height=2,
                              font=(FONT, 11, "bold"), bd=0, cursor="hand2",
                              activebackground=TEAL_DK, activeforeground="white",
                              command=commit_and_calculate_bill)
    save_billing_btn.pack(pady=15)
    _hover(save_billing_btn, TEAL, TEAL_DK)

    result_label = Label(billing_win, text="", font=(FONT, 14, "bold"), bg=APP_BG, fg=TEAL_DK)
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
root.config(bg=APP_BG)

# ---------------- TTK CLINICAL STYLING ----------------
_style = ttk.Style(root)
try:
    _style.theme_use("clam")
except Exception:
    pass
_style.configure("Treeview", font=(FONT, 10), rowheight=28, background=CARD_BG,
                 fieldbackground=CARD_BG, foreground=TEXT_DARK, borderwidth=0)
_style.configure("Treeview.Heading", font=(FONT, 10, "bold"), background=NAVY,
                 foreground="white", relief="flat", padding=6)
_style.map("Treeview.Heading", background=[("active", TEAL)])
_style.map("Treeview", background=[("selected", TEAL)], foreground=[("selected", "white")])
_style.configure("TCombobox", font=(FONT, 10), padding=4)

# ---------------- TITLES (gradient header banner) ----------------
header_canvas = Canvas(root, width=1200, height=104, highlightthickness=0, bd=0)
header_canvas.pack(fill=X)
draw_horizontal_gradient(header_canvas, 1200, 104, NAVY, TEAL)
header_canvas.create_text(46, 40, anchor="w", text="\u271a", font=(FONT, 26, "bold"), fill=ACCENT)
header_canvas.create_text(
    86, 42, anchor="w",
    text="SIERRA LEONE COMMUNITY HEALTH MANAGEMENT SYSTEM",
    font=(FONT, 20, "bold"), fill="white"
)
header_canvas.create_text(
    88, 74, anchor="w",
    text="Welcome to the Digital Clinic Management Platform",
    font=(FONT, 12), fill="#CBD9E6"
)

# ---------------- MAIN DASHBOARD PANEL CONTAINER ----------------
dashboard_container_frame = Frame(root, bg=APP_BG, width=1100, height=480)
dashboard_container_frame.pack(pady=18)
dashboard_container_frame.pack_propagate(False)

# ---- LEFT SIDE: MENU NAVIGATION SYSTEM PANELS ----
menu_frame = LabelFrame(dashboard_container_frame, text=" System Operations Menu ", font=(FONT, 11, "bold"),
                        bg=CARD_BG, fg=NAVY, padx=20, pady=20,
                        highlightbackground=BORDER, highlightthickness=1, relief="flat")
menu_frame.place(x=30, y=20, width=450, height=420)

btn_patient = Button(menu_frame, text="\U0001F464 Patient Registration", width=22, height=2, font=(FONT, 9, "bold"),
                     bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                     command=open_patient_window)
btn_patient.grid(row=0, column=0, padx=6, pady=14)
_hover(btn_patient, NAVY, TEAL)

btn_doctor = Button(menu_frame, text="\U0001FA7A Doctor Management", width=22, height=2, font=(FONT, 9, "bold"),
                    bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                    command=open_doctor_window)
btn_doctor.grid(row=1, column=0, padx=6, pady=14)
_hover(btn_doctor, NAVY, TEAL)

btn_manage = Button(menu_frame, text="\U0001F4C2 Record Management", width=22, height=2, font=(FONT, 9, "bold"),
                    bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                    command=open_record_management_window)
btn_manage.grid(row=0, column=1, padx=6, pady=14)
_hover(btn_manage, NAVY, TEAL)

btn_consult = Button(menu_frame, text="\U0001F4DD Consultation Desk", width=22, height=2, font=(FONT, 9, "bold"),
                     bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                     command=open_consultation_window)
btn_consult.grid(row=1, column=1, padx=6, pady=14)
_hover(btn_consult, NAVY, TEAL)

btn_billing = Button(menu_frame, text="\U0001F4B3 Billing Operations", width=22, height=2, font=(FONT, 9, "bold"),
                     bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                     command=open_billing_window)
btn_billing.grid(row=2, column=0, padx=6, pady=14)
_hover(btn_billing, NAVY, TEAL)

btn_reports = Button(menu_frame, text="\U0001F4CA Reports & Analytics", width=22, height=2, font=(FONT, 9, "bold"),
                     bg=NAVY, fg="white", bd=0, cursor="hand2", activebackground=TEAL, activeforeground="white",
                     command=open_reports_window)
btn_reports.grid(row=2, column=1, padx=6, pady=14)
_hover(btn_reports, NAVY, TEAL)


# ---- RIGHT SIDE: DASHBOARD STATISTICS & REPORT SUMMARY CARD BLOCKS ----
stats_frame = LabelFrame(dashboard_container_frame, text=" Live Facility Analytical Overview ",
                         font=(FONT, 11, "bold"), bg=CARD_BG, fg=NAVY, padx=20, pady=20,
                         highlightbackground=BORDER, highlightthickness=1, relief="flat")
stats_frame.place(x=520, y=20, width=540, height=420)

# Card 1: Patients Total
card1 = Frame(stats_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
card1.place(x=15, y=15, width=225, height=110)
Frame(card1, bg=C_BLUE, height=4).pack(fill=X)
Label(card1, text="TOTAL REGISTERED PATIENTS", font=(FONT, 9, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(pady=(14, 2))
lbl_stat_patients = Label(card1, text="0", font=(FONT, 26, "bold"), bg=CARD_BG, fg=C_BLUE)
lbl_stat_patients.pack()

# Card 2: Active Doctors
card2 = Frame(stats_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
card2.place(x=265, y=15, width=225, height=110)
Frame(card2, bg=C_TEAL, height=4).pack(fill=X)
Label(card2, text="ACTIVE CLINICAL DOCTORS", font=(FONT, 9, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(pady=(14, 2))
lbl_stat_doctors = Label(card2, text="0", font=(FONT, 26, "bold"), bg=CARD_BG, fg=C_TEAL)
lbl_stat_doctors.pack()

# Card 3: Total Consultations Completed
card3 = Frame(stats_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
card3.place(x=15, y=140, width=225, height=110)
Frame(card3, bg=C_AMBER, height=4).pack(fill=X)
Label(card3, text="CONSULTATIONS LOGGED", font=(FONT, 9, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(pady=(14, 2))
lbl_stat_consults = Label(card3, text="0", font=(FONT, 26, "bold"), bg=CARD_BG, fg=C_AMBER)
lbl_stat_consults.pack()

# Card 4: Financial Collections Aggregate
card4 = Frame(stats_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
card4.place(x=265, y=140, width=225, height=110)
Frame(card4, bg=C_VIOLET, height=4).pack(fill=X)
Label(card4, text="TOTAL MEDICAL INVOICES", font=(FONT, 9, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(pady=(14, 2))
lbl_stat_rev = Label(card4, text="Le 0.00", font=(FONT, 18, "bold"), bg=CARD_BG, fg=C_VIOLET)
lbl_stat_rev.pack(pady=4)

# Quick System Manual Checklist Label
Manual_label = Label(stats_frame,
                     text="\U0001F4A1 Quick Tip: Metrics update instantly whenever data is safely saved\nacross registration forms, consultation logs, or processing desks.",
                     font=(FONT, 9, "italic"), bg=CARD_BG, fg=TEXT_MUTE, justify=LEFT)
Manual_label.place(x=15, y=275)

# Refresh button to trigger updates on user demand
btn_refresh = Button(stats_frame, text="\U0001F504 Recalculate Statistics", font=(FONT, 10, "bold"), bg=TEAL,
                     fg="white", bd=0, activebackground=TEAL_DK, activeforeground="white", cursor="hand2",
                     command=refresh_dashboard_metrics)
btn_refresh.place(x=15, y=322, width=475, height=38)
_hover(btn_refresh, TEAL, TEAL_DK)

# ---------------- EXIT INFRASTRUCTURE ----------------
exit_btn = Button(root, text="Exit System Infrastructure", font=(FONT, 12, "bold"), bg=DANGER, fg="white",
                  padx=10, pady=4, bd=0, command=root.destroy, cursor="hand2",
                  activebackground="#B23A35", activeforeground="white")
exit_btn.pack(pady=10)
_hover(exit_btn, DANGER, "#B23A35")

# Initialize counts upon system launching
refresh_dashboard_metrics()

# ---------------- RUN INFRASTRUCTURE ENGINE ----------------
root.mainloop()
