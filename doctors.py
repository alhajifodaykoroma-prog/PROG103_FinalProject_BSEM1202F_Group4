import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from utils import generate_doctor_code


# ---------------- Database Engine Reader ----------------
def get_db_connection():
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------- Open Doctor Window ----------------
def open_doctor_window():

    root = Toplevel()
    root.title("Doctor Management Registry")
    root.geometry("600x480")
    root.config(bg="#F2F4F4")

    # Variables
    name_var = StringVar()
    phone_var = StringVar()
    avail_var = StringVar(value="08:00 - 16:00")


    # ---------------- Save Doctor Action ----------------
    def save_doctor():

        doctor_code = generate_doctor_code()

        doctor_name = name_var.get().strip()
        specialization = spec_combo.get().strip()
        phone = phone_var.get().strip()
        availability = avail_var.get().strip()

        if not doctor_name:
            messagebox.showerror(
                "Validation Error",
                "Doctor Name is required."
            )
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM doctors
            WHERE doctor_name=? AND specialization=?
            """,
            (doctor_name, specialization)
        )

        if cursor.fetchone():
            messagebox.showerror(
                "Duplicate Entry",
                "Doctor already exists."
            )
            conn.close()
            return

        try:

            cursor.execute(
                """
                INSERT INTO doctors
                (
                doctor_code,
                doctor_name,
                specialization,
                phone,
                availability,
                employment_status
                )
                VALUES (?, ?, ?, ?, ?,?)
                """,
                (
                    doctor_code,
                    doctor_name,
                    specialization,
                    phone,
                    availability,
                    "Active"
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Doctor Registered Successfully!\nDoctor ID: {doctor_code}"
            )

            root.destroy()

        except sqlite3.Error as err:

            messagebox.showerror(
                "Database Failure",
                str(err)
            )

        finally:
            conn.close()


    # Header
    Label(
        root,
        text="DOCTOR MANAGEMENT REGISTRY",
        font=("Arial",14,"bold"),
        bg="#2C3E50",
        fg="white",
        pady=10
    ).pack(fill=X)


    frame = Frame(
        root,
        bg="white",
        padx=20,
        pady=20,
        highlightbackground="#BDC3C7",
        highlightthickness=1
    )

    frame.pack(pady=25)


    Label(
        frame,
        text="Doctor Full Name *",
        bg="white"
    ).grid(row=0,column=0,pady=15,sticky=W)

    Entry(
        frame,
        textvariable=name_var,
        width=30
    ).grid(row=0,column=1,pady=15)


    Label(
        frame,
        text="Medical Specialization",
        bg="white"
    ).grid(row=1,column=0,pady=15,sticky=W)

    spec_combo = ttk.Combobox(
        frame,
        values=[
            "General Doctor",
            "Dentist",
            "Cardiologist",
            "Pediatrician",
            "Surgeon"
        ],
        width=27,
        state="readonly"
    )

    spec_combo.set("General Doctor")
    spec_combo.grid(row=1,column=1,pady=15)


    Label(
        frame,
        text="Contact Phone Number",
        bg="white"
    ).grid(row=2,column=0,pady=15,sticky=W)

    Entry(
        frame,
        textvariable=phone_var,
        width=30
    ).grid(row=2,column=1,pady=15)


    Label(
        frame,
        text="Availability Hours",
        bg="white"
    ).grid(row=3,column=0,pady=15,sticky=W)

    Entry(
        frame,
        textvariable=avail_var,
        width=30
    ).grid(row=3,column=1,pady=15)


    Button(
        root,
        text="Register Doctor Details",
        bg="#2C3E50",
        fg="white",
        font=("Arial",11,"bold"),
        padx=15,
        pady=8,
        command=save_doctor
    ).pack(pady=10)



# Testing mode only
if __name__ == "__main__":
    test_root = Tk()
    test_root.withdraw()
    open_doctor_window()
    test_root.mainloop()