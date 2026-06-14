import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
APP_BG    = "#EEF3F8"
CARD_BG   = "#FFFFFF"
BORDER    = "#D7E0EC"
TEXT_DARK = "#0F2440"
TEXT_MUTE = "#64748B"
C_BLUE    = "#2563EB"
C_TEAL    = "#0EA5A4"
C_AMBER   = "#E08A1E"
FONT      = "Lato"


# ---------------- Database Engine Reader ----------------
def get_db_connection():
    """Establishes an isolated connection to the clinic SQLite file with foreign keys enabled."""
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def fetch_report_data():
    """Queries aggregation analytics directly from live database structures."""
    conn = get_db_connection()
    cursor = conn.cursor()

    analytics = {
        "total_patients": 0,
        "total_consultations": 0,
        "total_revenue": 0.0,
        "top_diagnoses": []
    }

    try:
        # 1. Gather Total Patient Registration Volume
        cursor.execute("SELECT COUNT(*) FROM patients")
        analytics["total_patients"] = cursor.fetchone()[0]

        # 2. Gather Total Processed Consultations
        cursor.execute("SELECT COUNT(*) FROM consultations")
        analytics["total_consultations"] = cursor.fetchone()[0]

        # 3. Gather Combined Realized Gross Revenues (Sum of Invoice Net Values)
        cursor.execute("SELECT SUM(total_bill) FROM billing")
        sum_res = cursor.fetchone()[0]
        analytics["total_revenue"] = sum_res if sum_res is not None else 0.0

        # 4. Extract Top Frequently Recurring Diagnoses for clinic logistics mapping
        cursor.execute("""
            SELECT diagnosis, COUNT(diagnosis) as occurrences 
            FROM consultations 
            WHERE diagnosis IS NOT NULL AND diagnosis != ''
            GROUP BY diagnosis 
            ORDER BY occurrences DESC 
            LIMIT 5
        """)
        analytics["top_diagnoses"] = cursor.fetchall()

    except sqlite3.Error as db_error:
        messagebox.showerror("Metrics Error", f"Failed to parse reporting analytics tables: {db_error}")
    finally:
        conn.close()

    return analytics


def refresh_report_view():
    """Re-queries the database engine and updates data visual text targets dynamically."""
    fresh_data = fetch_report_data()

    lbl_patients_val.config(text=f"{fresh_data['total_patients']}")
    lbl_consults_val.config(text=f"{fresh_data['total_consultations']}")
    lbl_revenue_val.config(text=f"Le {fresh_data['total_revenue']:,.2f}")

    # Refresh the Treeview list rows
    for item in table_diagnoses.get_children():
        table_diagnoses.delete(item)

    for rank, (diag, count) in enumerate(fresh_data["top_diagnoses"], start=1):
        table_diagnoses.insert("", END, values=(rank, diag, count))


# ---------------- UI Interface Layout Structure ----------------
root = Tk()
root.title("Sierra Leone Community Health Reporting Engine")
root.geometry("900x650")
root.config(bg=APP_BG)
root.option_add("*Font", (FONT, 10))

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

# App Window Main Top Ribbon Header banner
Label(
    root,
    text="CLINICAL ANALYTICS & STATISTICAL REPORTS",
    font=(FONT, 16, "bold"),
    bg=NAVY,
    fg="white",
    pady=15
).pack(fill=X)

# Metrics Grid Container Layout Frame
metrics_frame = Frame(root, bg=APP_BG)
metrics_frame.pack(pady=30)

# Card block 1: Patient Tracking Metrics Card
card_patients = Frame(metrics_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1, width=240,
                      height=120)
card_patients.grid(row=0, column=0, padx=15)
card_patients.pack_propagate(False)
Label(card_patients, text="TOTAL REGISTERED PATIENTS", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(
    pady=15)
lbl_patients_val = Label(card_patients, text="0", font=(FONT, 22, "bold"), bg=CARD_BG, fg=C_BLUE)
lbl_patients_val.pack()

# Card block 2: Medical Cases Volume Metrics Card
card_consults = Frame(metrics_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1, width=240,
                      height=120)
card_consults.grid(row=0, column=1, padx=15)
card_consults.pack_propagate(False)
Label(card_consults, text="TOTAL CONSULTATIONS LOGGED", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(
    pady=15)
lbl_consults_val = Label(card_consults, text="0", font=(FONT, 22, "bold"), bg=CARD_BG, fg=C_TEAL)
lbl_consults_val.pack()

# Card block 3: Gross Revenue Tracking Metrics Card
card_revenue = Frame(metrics_frame, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1, width=260,
                     height=120)
card_revenue.grid(row=0, column=2, padx=15)
card_revenue.pack_propagate(False)
Label(card_revenue, text="COMBINED REVENUE INVOICED", font=(FONT, 10, "bold"), bg=CARD_BG, fg=TEXT_MUTE).pack(
    pady=15)
lbl_revenue_val = Label(card_revenue, text="Le 0.00", font=(FONT, 18, "bold"), bg=CARD_BG, fg=C_AMBER)
lbl_revenue_val.pack()

# Lower Section - Data Table layout for common diagnoses patterns
table_frame = Frame(root, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER, highlightthickness=1)
table_frame.pack(pady=10, fill=BOTH, expand=True, padx=45)

Label(table_frame, text="Top Epidemiological Case Distributions (Highest Frequency)", font=(FONT, 12, "bold"),
      bg=CARD_BG, fg=NAVY).pack(anchor=W, pady=5)

# Generate column matrix treeview mapping details
columns_map = ("rank", "diagnosis", "cases")
table_diagnoses = ttk.Treeview(table_frame, columns=columns_map, show="headings", height=6)
table_diagnoses.pack(fill=BOTH, expand=True, side=LEFT)

table_diagnoses.heading("rank", text="Rank Pos")
table_diagnoses.heading("diagnosis", text="Medical Condition / Diagnosis Path")
table_diagnoses.heading("cases", text="Total Tracked Occurrences")

table_diagnoses.column("rank", width=80, anchor=CENTER)
table_diagnoses.column("diagnosis", width=400, anchor=W)
table_diagnoses.column("cases", width=150, anchor=CENTER)

# Scroll widget configuration allocation mapping
scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=table_diagnoses.yview)
table_diagnoses.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

# Operational Window bottom structural utility buttons row elements
button_frame = Frame(root, bg=APP_BG)
button_frame.pack(pady=25)

Button(button_frame, text="🔄 Synchronize Live Metrics Data", font=(FONT, 11, "bold"), bg=TEAL, fg="white",
       bd=0, cursor="hand2", activebackground=TEAL_DK, activeforeground="white",
       padx=15, pady=8, command=refresh_report_view).grid(row=0, column=0, padx=10)
Button(button_frame, text="❌ Close Reports View", font=(FONT, 11, "bold"), bg="#7F8C8D", fg="white",
       bd=0, cursor="hand2", activebackground="#5F6B72", activeforeground="white", padx=15, pady=8,
       command=root.destroy).grid(row=0, column=1, padx=10)

# Execute baseline system seed generation checks right away upon startup mapping
refresh_report_view()

root.mainloop()