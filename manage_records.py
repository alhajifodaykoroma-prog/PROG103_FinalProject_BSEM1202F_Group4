import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
APP_BG    = "#EEF3F8"
CARD_BG   = "#FFFFFF"
BORDER    = "#D7E0EC"
FONT      = "Lato"


def _hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------- MAIN MANAGEMENT WINDOW ----------------
def open_record_management_window():
    manage_win = Toplevel()
    manage_win.title("Professional Record Management")
    manage_win.geometry("1250x750")
    manage_win.config(bg=APP_BG)
    manage_win.option_add("*Font", (FONT, 10))
    manage_win.option_add("*Entry.relief", "solid")
    manage_win.option_add("*Entry.borderWidth", "1")
    manage_win.option_add("*Entry.highlightThickness", "0")

    # =====================================================
    # PATIENT SECTION
    # =====================================================
    patient_frame = LabelFrame(
        manage_win,
        text=" Patient Record Management ",
        padx=10,
        pady=10,
        bg="white",
        font=(FONT, 11, "bold"),
        fg=NAVY
    )
    patient_frame.pack(fill=X, padx=10, pady=5)

    # ---- SEARCH CONTROLS FOR PATIENTS ----
    p_search_frame = Frame(patient_frame, bg="white")
    p_search_frame.pack(fill=X, pady=5)

    Label(p_search_frame, text="🔍 Search Patient (Name/ID):", font=("Arial", 10), bg="white").pack(side=LEFT, padx=5)
    patient_search_var = StringVar()
    patient_search_entry = Entry(p_search_frame, textvariable=patient_search_var, width=30)
    patient_search_entry.pack(side=LEFT, padx=5)

    patient_tree = ttk.Treeview(
        patient_frame,
        columns=("ID", "Name", "Phone", "Status"),
        show="headings",
        height=6
    )

    patient_tree.heading("ID", text="Patient ID")
    patient_tree.heading("Name", text="Full Name")
    patient_tree.heading("Phone", text="Phone")
    patient_tree.heading("Status", text="Status")

    patient_tree.column("ID", width=100)
    patient_tree.column("Name", width=300)
    patient_tree.column("Phone", width=180)
    patient_tree.column("Status", width=150)
    patient_tree.pack(fill=X, pady=5)

    # ---- EDIT/UPDATE FIELD INTERFACES FOR PATIENTS ----
    p_edit_frame = Frame(patient_frame, bg="#F8F9F9", bd=1, relief=SUNKEN, pady=5)
    p_edit_frame.pack(fill=X, pady=5)

    Label(p_edit_frame, text="Selected Name:", bg="#F8F9F9").grid(row=0, column=0, padx=5, sticky=W)
    p_name_var = StringVar()
    Entry(p_edit_frame, textvariable=p_name_var, width=25).grid(row=0, column=1, padx=5)

    Label(p_edit_frame, text="Selected Phone:", bg="#F8F9F9").grid(row=0, column=2, padx=5, sticky=W)
    p_phone_var = StringVar()
    Entry(p_edit_frame, textvariable=p_phone_var, width=20).grid(row=0, column=3, padx=5)

    # ---------------- LOAD/FILTER PATIENTS ----------------
    def load_patients(*args):
        for item in patient_tree.get_children():
            patient_tree.delete(item)

        conn = get_db_connection()
        cursor = conn.cursor()

        search_query = patient_search_var.get().strip()
        if search_query:
            cursor.execute(
                """
                SELECT patient_id, full_name, phone, status
                FROM patients
                WHERE full_name LIKE ? OR patient_id LIKE ?
                ORDER BY patient_id DESC
                """,
                (f"%{search_query}%", f"%{search_query}%")
            )
        else:
            cursor.execute(
                """
                SELECT patient_id, full_name, phone, status
                FROM patients
                ORDER BY patient_id DESC
                """
            )

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            patient_tree.insert("", END, values=row)

    # Trigger patient auto-filtering as user types
    patient_search_var.trace_add("write", load_patients)

    # Auto-fill patient entry fields on table selection
    def on_patient_select(event):
        selected = patient_tree.selection()
        if selected:
            item = patient_tree.item(selected[0])
            values = item["values"]
            p_name_var.set(values[1])
            p_phone_var.set(values[2])

    patient_tree.bind("<<TreeviewSelect>>", on_patient_select)

    # ---------------- UPDATE PATIENT BASE DETAILS (EDIT) ----------------
    def update_patient_details():
        selected = patient_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a patient from the table to modify.")
            return

        p_id = patient_tree.item(selected[0])["values"][0]
        new_name = p_name_var.get().strip()
        new_phone = p_phone_var.get().strip()

        if not new_name or not new_phone:
            messagebox.showerror("Validation Error", "Fields cannot be blank during modifications.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE patients SET full_name=?, phone=? WHERE patient_id=?",
            (new_name, new_phone, p_id)
        )
        conn.commit()
        conn.close()

        load_patients()
        messagebox.showinfo("Success", "Patient profile details updated completely.")

    # ---------------- CHANGE PATIENT STATUS ----------------
    def change_patient_status(new_status):
        selected = patient_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a patient.")
            return

        item = patient_tree.item(selected[0])
        patient_id = item["values"][0]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET status=? WHERE patient_id=?", (new_status, patient_id))
        conn.commit()
        conn.close()

        load_patients()
        messagebox.showinfo("Success", f"Patient status changed to '{new_status}'.")

    # Command Execution Buttons Layout
    patient_button_frame = Frame(patient_frame, bg="white")
    patient_button_frame.pack(pady=5)

    Button(patient_button_frame, text="📝 Save Field Changes (Edit)", bg=TEAL, fg="white",
           font=(FONT, 10, "bold"), bd=0, cursor="hand2", activebackground=TEAL_DK, activeforeground="white",
           command=update_patient_details).grid(row=0, column=0, padx=15)
    Button(patient_button_frame, text="Set Active", bg="green", fg="white",
           command=lambda: change_patient_status("Active")).grid(row=0, column=1, padx=5)
    Button(patient_button_frame, text="Set Discharged", bg="orange", fg="white",
           command=lambda: change_patient_status("Discharged")).grid(row=0, column=2, padx=5)
    Button(patient_button_frame, text="Set Deceased", bg="red", fg="white",
           command=lambda: change_patient_status("Deceased")).grid(row=0, column=3, padx=5)

    # =====================================================
    # DOCTOR SECTION
    # =====================================================
    doctor_frame = LabelFrame(
        manage_win,
        text=" Doctor Management ",
        padx=10,
        pady=10,
        bg="white",
        font=(FONT, 11, "bold"),
        fg=NAVY
    )
    doctor_frame.pack(fill=X, padx=10, pady=5)

    # ---- SEARCH CONTROLS FOR DOCTORS ----
    d_search_frame = Frame(doctor_frame, bg="white")
    d_search_frame.pack(fill=X, pady=5)

    Label(d_search_frame, text="🔍 Search Doctor (Name/ID):", font=("Arial", 10), bg="white").pack(side=LEFT, padx=5)
    doctor_search_var = StringVar()
    doctor_search_entry = Entry(d_search_frame, textvariable=doctor_search_var, width=30)
    doctor_search_entry.pack(side=LEFT, padx=5)

    doctor_tree = ttk.Treeview(
        doctor_frame,
        columns=("ID", "Name", "Specialization", "Status"),
        show="headings",
        height=6
    )

    doctor_tree.heading("ID", text="Doctor ID")
    doctor_tree.heading("Name", text="Doctor Name")
    doctor_tree.heading("Specialization", text="Specialization")
    doctor_tree.heading("Status", text="Employment Status")

    doctor_tree.column("ID", width=100)
    doctor_tree.column("Name", width=300)
    doctor_tree.column("Specialization", width=250)
    doctor_tree.column("Status", width=180)
    doctor_tree.pack(fill=X, pady=5)

    # ---- EDIT/UPDATE FIELD INTERFACES FOR DOCTORS ----
    d_edit_frame = Frame(doctor_frame, bg="#F8F9F9", bd=1, relief=SUNKEN, pady=5)
    d_edit_frame.pack(fill=X, pady=5)

    Label(d_edit_frame, text="Doctor Name:", bg="#F8F9F9").grid(row=0, column=0, padx=5, sticky=W)
    d_name_var = StringVar()
    Entry(d_edit_frame, textvariable=d_name_var, width=25).grid(row=0, column=1, padx=5)

    Label(d_edit_frame, text="Specialization:", bg="#F8F9F9").grid(row=0, column=0, padx=5, sticky=W)
    d_spec_var = StringVar()
    Entry(d_edit_frame, textvariable=d_spec_var, width=25).grid(row=0, column=4, padx=5)

    # ---------------- LOAD/FILTER DOCTORS ----------------
    def load_doctors(*args):
        for item in doctor_tree.get_children():
            doctor_tree.delete(item)

        conn = get_db_connection()
        cursor = conn.cursor()

        search_query = doctor_search_var.get().strip()
        if search_query:
            cursor.execute(
                """
                SELECT doctor_id, doctor_name, specialization, employment_status
                FROM doctors
                WHERE doctor_name LIKE ? OR doctor_id LIKE ?
                ORDER BY doctor_id DESC
                """,
                (f"%{search_query}%", f"%{search_query}%")
            )
        else:
            cursor.execute(
                """
                SELECT doctor_id, doctor_name, specialization, employment_status
                FROM doctors
                ORDER BY doctor_id DESC
                """
            )

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            doctor_tree.insert("", END, values=row)

    # Trigger doctor filtering on keypress events
    doctor_search_var.trace_add("write", load_doctors)

    # Auto-fill doctor fields on table selection row highlight
    def on_doctor_select(event):
        selected = doctor_tree.selection()
        if selected:
            item = doctor_tree.item(selected[0])
            values = item["values"]
            d_name_var.set(values[1])
            d_spec_var.set(values[2])

    doctor_tree.bind("<<TreeviewSelect>>", on_doctor_select)

    # ---------------- UPDATE DOCTOR DETAILS (EDIT) ----------------
    def update_doctor_details():
        selected = doctor_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a professional row tracker to edit details.")
            return

        d_id = doctor_tree.item(selected[0])["values"][0]
        new_name = d_name_var.get().strip()
        new_spec = d_spec_var.get().strip()

        if not new_name or not new_spec:
            messagebox.showerror("Validation Error", "Inputs cannot look completely empty.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctors SET doctor_name=?, specialization=? WHERE doctor_id=?",
            (new_name, new_spec, d_id)
        )
        conn.commit()
        conn.close()

        load_doctors()
        messagebox.showinfo("Success", "Doctor configuration details successfully updated.")

    # ---------------- CHANGE DOCTOR STATUS ----------------
    def change_doctor_status(new_status):
        selected = doctor_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a doctor.")
            return

        item = doctor_tree.item(selected[0])
        doctor_id = item["values"][0]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE doctors SET employment_status=? WHERE doctor_id=?", (new_status, doctor_id))
        conn.commit()
        conn.close()

        load_doctors()
        messagebox.showinfo("Success", f"Doctor status changed to '{new_status}'.")

    # Action layout controls
    doctor_button_frame = Frame(doctor_frame, bg="white")
    doctor_button_frame.pack(pady=5)

    Button(doctor_button_frame, text="📝 Save Field Changes (Edit)", bg=TEAL, fg="white",
           font=(FONT, 10, "bold"), bd=0, cursor="hand2", activebackground=TEAL_DK, activeforeground="white",
           command=update_doctor_details).grid(row=0, column=0, padx=15)
    Button(doctor_button_frame, text="Set Active", bg="green", fg="white",
           command=lambda: change_doctor_status("Active")).grid(row=0, column=1, padx=5)
    Button(doctor_button_frame, text="Set Retired", bg="orange", fg="white",
           command=lambda: change_doctor_status("Retired")).grid(row=0, column=2, padx=5)
    Button(doctor_button_frame, text="Set Suspended", bg="red", fg="white",
           command=lambda: change_doctor_status("Suspended")).grid(row=0, column=3, padx=5)

    # Load defaults instantly upon layout construction
    load_patients()
    load_doctors()