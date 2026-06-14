import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
CARD_BG   = "#FFFFFF"
FONT      = "Lato"


def _hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


# ---------------- Database Connections ----------------
def get_connection():
    """Establishes a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def load_patients():
    """Fetches real records from the patients table to populate the dropdown."""
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


def refresh_patient_dropdown(*_):
    """Refreshes patient dropdown list dynamically when clicked."""
    fresh_patients = load_patients()
    patient_combo["values"] = [f"{row[0]} - {row[1]}" for row in fresh_patients]


# ---------------- Calculate & Save Bill ----------------
def calculate_bill():
    # Validation: Ensure a patient was actually chosen from the list
    if not patient_combo.get().strip():
        messagebox.showerror("Validation Error", "Please select a patient from the list.")
        return

    try:
        # Extract the numeric patient_id from the dropdown string format: "ID - Name"
        patient_id = patient_combo.get().split("-")[0].strip()

        # Gather numeric values safely
        consultation = consultation_var.get()
        medicine = medicine_var.get()
        treatment = treatment_var.get()

        total = consultation + medicine + treatment

        # Update the UI displaying total with Sierra Leonean currency notation (Le)
        result_label.config(text=f"Total Bill: Le {total:,.2f}")

        # Connect and insert into the exact columns defined in your database schema
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO billing
            (patient_id, consultation_fee, medicine_fee, treatment_fee, total_bill)
            VALUES (?, ?, ?, ?, ?)
            """,
            (patient_id, consultation, medicine, treatment, total),
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Bill Generated and Saved Successfully!")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid monetary numbers.")
    except Exception as err:
        messagebox.showerror("Database Error", f"An unexpected error occurred: {err}")


# ---------------- UI Window Architecture ----------------
root = Tk()
root.title("Billing System")
root.geometry("800x600")
root.config(bg="#F8F9F9")
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

# Form variables
patient_var = StringVar()
consultation_var = DoubleVar(value=0.0)
medicine_var = DoubleVar(value=0.0)
treatment_var = DoubleVar(value=0.0)

# Heading
Label(
    root, text="BILLING SYSTEM", font=(FONT, 18, "bold"), bg=NAVY, fg="white", pady=16
).pack(fill=X)

frame = Frame(root, bg="white", padx=20, pady=20)
frame.pack(pady=20)

# Form Fields Layout
Label(frame, text="Select Patient", bg="white").grid(
    row=0, column=0, pady=10, sticky=W
)
patient_combo = ttk.Combobox(frame, width=32)
patient_combo.grid(row=0, column=1)

# Seed initial patient drop-down values and attach the click-to-refresh binding
initial_patients = load_patients()
patient_combo["values"] = [f"{row[0]} - {row[1]}" for row in initial_patients]
patient_combo.bind("<Button-1>", refresh_patient_dropdown)

Label(frame, text="Consultation Fee (Le)", bg="white").grid(
    row=1, column=0, pady=10, sticky=W
)
Entry(frame, textvariable=consultation_var, width=35).grid(row=1, column=1)

Label(frame, text="Medicine Fee (Le)", bg="white").grid(
    row=2, column=0, pady=10, sticky=W
)
Entry(frame, textvariable=medicine_var, width=35).grid(row=2, column=1)

Label(frame, text="Treatment Fee (Le)", bg="white").grid(
    row=3, column=0, pady=10, sticky=W
)
Entry(frame, textvariable=treatment_var, width=35).grid(row=3, column=1)

# Execution Button
calculate_bill_btn = Button(
    root,
    text="Calculate & Save Bill",
    bg=TEAL,
    fg="white",
    bd=0,
    cursor="hand2",
    activebackground=TEAL_DK,
    activeforeground="white",
    font=(FONT, 11, "bold"),
    width=25,
    height=2,
    command=calculate_bill,
)
calculate_bill_btn.pack(pady=20)
_hover(calculate_bill_btn, TEAL, TEAL_DK)

# Output Total display
result_label = Label(
    root, text="", font=(FONT, 14, "bold"), bg="#F8F9F9", fg=TEAL_DK
)
result_label.pack(pady=10)

root.mainloop()