import sqlite3
import os
import shutil
from datetime import datetime


# =====================================================
# AUTOMATED DATABASE BACKUP ENGINE
# =====================================================
def create_database_backup():
    """
    Creates a secure, timestamped backup copy of clinic.db
    inside a dedicated 'backups' directory.
    """
    db_file = "clinic.db"
    backup_dir = "backups"

    # Check if the primary database file exists before backing it up
    if os.path.exists(db_file):
        try:
            # Create the backup folder if it does not exist
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                print(f"Created dedicated directory: '{backup_dir}/'")

            # Generate a distinct timestamp label (Year-Month-Day_Hour-Minute-Second)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Perform a safe structural file copy operation
            shutil.copy2(db_file, backup_path)
            print(f"💾 SECURITY BACKUP CREATED: Saved as '{backup_path}'")

        except Exception as error:
            print(f"⚠️ Backup Warning: Could not create snapshot: {error}")
    else:
        print("ℹ️ No existing database file found to backup. Skipping copy process...")


# =====================================================
# STRUCTURAL DATABASE SCHEMA UPGRADES
# =====================================================

# 1. Run the backup protocol before executing updates
create_database_backup()

# 2. Establish connection to database
conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# ----------- PATIENT STATUS UPGRADE ----------
try:
    cursor.execute(
        """
        ALTER TABLE patients
        ADD COLUMN status TEXT DEFAULT 'Active'
        """
    )
    print("Patient Status column added successfully.")
except sqlite3.OperationalError:
    print("Patient Status column already exists.")

# ------- DOCTOR STATUS UPGRADE --------------
try:
    cursor.execute(
        """
        ALTER TABLE doctors
        ADD COLUMN employment_status TEXT DEFAULT 'Active'
        """
    )
    print("Doctor employment status column added successfully.")
except sqlite3.OperationalError:
    print("Doctor status column already exists.")

# ---- FIXED CONNECTION MANAGEMENT (Out of the except block) ----
conn.commit()
conn.close()

print("\n🚀 Database processing and upgrades completed successfully.")