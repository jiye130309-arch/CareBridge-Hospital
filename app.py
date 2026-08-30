from datetime import date, datetime, timedelta
import re
import sqlite3
#import flask
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = "carebridge.db"
# Staff departments available for appointment booking
STAFF_DEPARTMENTS = ["GP", "Specialist"]
PATIENT_TYPES = ["Subsidised", "Private"]
# Patient billing categories
FIRST_AVAILABLE_OFFSET_DAYS = 8
# Minimum advance booking period (days)
BASE_CONSULTATION_FEE = 100
LAB_TEST_RATE = 10
SUBSIDISED_DISCOUNT = 0.30
# Billing rates and discounts

def get_db_connection():
    """Open the SQLite database used by CareBridge."""
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def get_column_names(connection, table_name):
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row["name"] for row in rows]


def create_tables():
    """Create tables if they do not already exist."""
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_type TEXT NOT NULL,
            lab_tests INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS triage_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity INTEGER NOT NULL,
            assigned_room TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    install_completed_patient_triggers(connection)
    connection.commit()
    connection.close()


def install_completed_patient_triggers(connection):
    """When status is saved as Completed in SQLite, delete that patient immediately."""
    connection.execute("DROP TRIGGER IF EXISTS trg_patient_gone_on_appt_completed_update")
    connection.execute("DROP TRIGGER IF EXISTS trg_patient_gone_on_appt_completed_insert")
    connection.execute(
        """
        CREATE TRIGGER trg_patient_gone_on_appt_completed_update
        AFTER UPDATE OF status ON appointments
        WHEN upper(trim(NEW.status)) = 'COMPLETED'
        BEGIN
            DELETE FROM patients
            WHERE (
                trim(coalesce(NEW.patient_code, '')) != ''
                AND upper(trim(patient_code)) = upper(trim(NEW.patient_code))
            )
            OR upper(trim(name)) = upper(trim(NEW.full_name));
        END
        """
    )
    connection.execute(
        """
        CREATE TRIGGER trg_patient_gone_on_appt_completed_insert
        AFTER INSERT ON appointments
        WHEN upper(trim(NEW.status)) = 'COMPLETED'
        BEGIN
            DELETE FROM patients
            WHERE (
                trim(coalesce(NEW.patient_code, '')) != ''
                AND upper(trim(patient_code)) = upper(trim(NEW.patient_code))
            )
            OR upper(trim(name)) = upper(trim(NEW.full_name));
        END
        """
    )


# Rebuild appointments table if column structure has changed
# Preserves existing patient data while updating schema
def migrate_appointments_table():
    """Rebuild appointments to the current booking columns, keeping existing rows."""
    connection = get_db_connection()

    tables = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    ]

    if "appointments" not in tables:
        connection.close()
        return

    current_columns = set(get_column_names(connection, "appointments"))

    wanted_columns = {
        "id",
        "patient_code",
        "full_name",
        "department",
        "appointment_date",
        "status",
        "created_at",
    }

    if current_columns == wanted_columns:
        connection.close()
        return

    connection.execute("DROP TABLE IF EXISTS appointments_new")

    connection.execute(
        """
        CREATE TABLE appointments_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
    )

    def existing_column(column, default):
        return column if column in current_columns else default

    connection.execute(
        f"""
        INSERT INTO appointments_new (
            id, patient_code, full_name, department, appointment_date, status, created_at
        )
        SELECT
            id,
            {existing_column("patient_code", "NULL")},
            full_name,
            department,
            appointment_date,
            {existing_column("status", "'Pending'")},
            created_at
        FROM appointments
        """
    )

    connection.execute("DROP TABLE appointments")
    connection.execute("ALTER TABLE appointments_new RENAME TO appointments")

    connection.commit()
    connection.close()

# Automatically removes patients whose appointments are marked 'Completed'
create_tables()
migrate_appointments_table()

# Rebuild triggers after migrate, because dropping appointments also drops them.
_trigger_connection = get_db_connection()
install_completed_patient_triggers(_trigger_connection)
_trigger_connection.commit()
_trigger_connection.close()


def now_text():
    return datetime.now().isoformat(timespec="seconds")


def first_error(checks):
    """Return the first error message. The form is shown again until input is valid."""
    for is_valid, message in checks:
        if not is_valid:
            return message
    return None


def is_real_patient_name(name):
    """A patient name must use letters, not numbers."""
    if name == "":
        return False
    letter_count = 0
    for character in name:
        if character.isdigit():
            return False
        if character.isalpha():
            letter_count += 1
        elif character not in " .'-":
            return False
    return letter_count >= 2


def is_valid_patient_id(patient_code):
    """Patient ID must be P001 onwards, for example P001, P002, P015."""
    match = re.fullmatch(r"P(\d{3,})", patient_code)
    if match is None:
        return False
    return int(match.group(1)) >= 1


def today_date():
    return date.today()


def first_available_appointment_date():
    """First bookable date: 8 days from today. Recalculated from the current date."""
    return today_date() + timedelta(days=FIRST_AVAILABLE_OFFSET_DAYS)


COMPLETED_APPOINTMENT_MATCH = """
    EXISTS (
        SELECT 1
          FROM appointments
         WHERE upper(trim(appointments.status)) = 'COMPLETED'
           AND (
                (
                    trim(coalesce(appointments.patient_code, '')) != ''
                    AND upper(trim(appointments.patient_code)) = upper(trim(patients.patient_code))
                )
             OR upper(trim(appointments.full_name)) = upper(trim(patients.name))
           )
    )
"""


def get_patients():
    remove_patients_with_completed_appointments()
    connection = get_db_connection()
    patients = connection.execute(
        f"""
        SELECT patient_code, name, age
          FROM patients
         WHERE NOT {COMPLETED_APPOINTMENT_MATCH}
         ORDER BY name
        """
    ).fetchall()
    connection.close()
    return patients


def list_registered_patients():
    """Patients still shown on Register. Completed appointments are excluded."""
    remove_patients_with_completed_appointments()
    connection = get_db_connection()
    patients = connection.execute(
        f"""
        SELECT patient_code, name, age
          FROM patients
         WHERE NOT {COMPLETED_APPOINTMENT_MATCH}
         ORDER BY id DESC
        """
    ).fetchall()
    connection.close()
    return patients


def remove_patients_with_completed_appointments():
    """If an appointment status is Completed in SQLite, remove that patient from the site."""
    connection = get_db_connection()
    connection.execute(
        f"""
        DELETE FROM patients
         WHERE {COMPLETED_APPOINTMENT_MATCH}
        """
    )
    connection.commit()
    connection.close()


def get_assigned_room(severity):
    if 1 <= severity <= 4:
        return "Waiting Room"
    if 5 <= severity <= 7:
        return "Room 1"
    return "Room 2"


@app.route("/")
def home():
    """Show the staff hospital management home page."""
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/doctors")
def doctors():
    return render_template("doctors.html")

# Get all registered patients
@app.route("/register", methods=["GET", "POST"])
def register_patient():
    """Register a patient and save the record in SQLite."""
    error_message = None
    success_message = None
    registered_patient = None
    form_data = {}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        patient_code = request.form.get("patient_code", "").strip().upper()
        form_data = request.form

        error_message = first_error(
            [
                (name != "", "Patient name cannot be blank."),
                (is_real_patient_name(name), "Patient name must be a real name. Numbers are not allowed."),
                (patient_code != "", "Patient ID cannot be blank."),
                (
                    is_valid_patient_id(patient_code),
                    "Patient ID must be in the format P001 onwards.",
                ),
                (
                    age_text.isdigit() and int(age_text) > 0,
                    "Age must be a positive whole number.",
                ),
            ]
        )

        if error_message is None:
            connection = get_db_connection()
            existing = connection.execute(
                "SELECT id FROM patients WHERE upper(patient_code) = ?",
                (patient_code,),
            ).fetchone()
            if existing:
                connection.close()
                error_message = "This Patient ID is already registered and cannot be used again."
            else:
                try:
                    connection.execute(
                        """
                        INSERT INTO patients (patient_code, name, age, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (patient_code, name, int(age_text), now_text()),
                    )
                    connection.commit()
                    connection.close()
                    success_message = "Patient registered successfully."
                    registered_patient = {
                        "name": name,
                        "age": int(age_text),
                        "patient_code": patient_code,
                    }
                    form_data = {}
                except sqlite3.IntegrityError:
                    connection.close()
                    error_message = "This Patient ID is already registered and cannot be used again."

    patients = list_registered_patients()

    return render_template(
        "register_patient.html",
        error_message=error_message,
        success_message=success_message,
        registered_patient=registered_patient,
        form_data=form_data,
        patients=patients,
    )


@app.route("/appointments", methods=["GET", "POST"])
def book_appointment():
    """Book an appointment for a registered patient."""
    error_message = None
    patients = get_patients()

    if request.method == "POST":
        department = request.form.get("department", "").strip()
        appointment_date_text = request.form.get("appointment_date", "").strip()
        patient_code = request.form.get("patient_code", "").strip()
        patient_name = ""
        # Calculate the earliest available appointment date
        first_available_date = first_available_appointment_date()
        
        # Check if the patient is registered
        connection = get_db_connection()
        patient = connection.execute(
            "SELECT patient_code, name FROM patients WHERE patient_code = ?",
            (patient_code,),
        ).fetchone()

        if patient is None:
            connection.close()
            error_message = "Please select a registered patient."
        else:
            patient_name = patient["name"]
             # Validate the department
            if department not in STAFF_DEPARTMENTS:
                connection.close()
                error_message = "Department must be GP or Specialist."
            else:
                try:
                    # Convert the entered date into a valid date
                    appointment_date = datetime.strptime(
                        appointment_date_text, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    # Display an error if the date format is invalid
                    connection.close()
                    error_message = "Please enter a valid appointment date in YYYY-MM-DD format."
                else:
                    # Check that the appointment is at least 8 days from today
                    if appointment_date < first_available_date:
                        connection.close()
                        error_message = (
                            "The appointment date must be at least 8 days from today."
                        )

        if error_message:
            return render_template(
                "appointments.html",
                departments=STAFF_DEPARTMENTS,
                patients=patients,
                form_data=request.form,
                error_message=error_message,
            )
        # Save the valid appointment into the database
        cursor = connection.execute(
            """
            INSERT INTO appointments (
                patient_code, full_name, department, appointment_date, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_code,
                patient_name,
                department,
                appointment_date_text,
                "Pending",
                now_text(),
            ),
        )
        # Commit the appointment and get its ID
        connection.commit()
        appointment_id = cursor.lastrowid
        connection.close()
        return redirect(url_for("appointment_confirmation", appointment_id=appointment_id))

    selected_code = request.args.get("patient_code", "").strip()
    form_data = {"patient_code": selected_code} if selected_code else {}

    return render_template(
        "appointments.html",
        departments=STAFF_DEPARTMENTS,
        patients=patients,
        form_data=form_data,
        error_message=None,
    )


@app.route("/appointments/confirmation/<int:appointment_id>")
def appointment_confirmation(appointment_id):
    """Show the saved appointment after a successful booking."""
    connection = get_db_connection()
    appointment = connection.execute(
        "SELECT * FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()
    connection.close()

    if appointment is None:
        return redirect(url_for("book_appointment"))

    return render_template("appointment_confirmation.html", appointment=appointment)


@app.route("/bill", methods=["GET", "POST"])
def calculate_bill():
    """Calculate a patient bill and save it in SQLite."""
    error_message = None
    bill_result = None
    form_data = {}

    if request.method == "POST":
        patient_type = request.form.get("patient_type", "").strip()
        lab_tests_text = request.form.get("lab_tests", "").strip()
        form_data = request.form

        if patient_type not in PATIENT_TYPES:
            error_message = "Patient type must be Subsidised or Private."
        elif not lab_tests_text.isdigit():
            error_message = "Number of laboratory tests must be a whole number."
        else:
            lab_tests = int(lab_tests_text)
            lab_test_cost = lab_tests * LAB_TEST_RATE
            subtotal = BASE_CONSULTATION_FEE + lab_test_cost
            discount = 0
            total = subtotal
            if patient_type == "Subsidised":
                discount = subtotal * SUBSIDISED_DISCOUNT
                total = subtotal * (1 - SUBSIDISED_DISCOUNT)

            connection = get_db_connection()
            connection.execute(
                """
                INSERT INTO bills (
                    patient_type, lab_tests, subtotal, discount, total, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (patient_type, lab_tests, subtotal, discount, total, now_text()),
            )
            connection.commit()
            connection.close()

            bill_result = {
                "patient_type": patient_type,
                "lab_tests": lab_tests,
                "base_fee": BASE_CONSULTATION_FEE,
                "lab_test_cost": lab_test_cost,
                "subtotal": subtotal,
                "discount": discount,
                "total": total,
            }
            form_data = {}

    return render_template(
        "bill.html",
        error_message=error_message,
        bill_result=bill_result,
        form_data=form_data,
        patient_types=PATIENT_TYPES,
        base_fee=BASE_CONSULTATION_FEE,
        lab_rate=LAB_TEST_RATE,
    )


@app.route("/triage", methods=["GET", "POST"])
def assign_triage_room():
    """Assign a triage room from a severity score of 1 to 10."""
    error_message = None
    triage_result = None
    form_data = {}

    if request.method == "POST":
        severity_text = request.form.get("severity", "").strip()
        form_data = request.form

        if not severity_text.isdigit():
            error_message = "Severity must be a whole number between 1 and 10."
        else:
            severity = int(severity_text)
            if severity < 1 or severity > 10:
                error_message = "Severity must be a whole number between 1 and 10."
            else:
                assigned_room = get_assigned_room(severity)
                connection = get_db_connection()
                connection.execute(
                    """
                    INSERT INTO triage_records (severity, assigned_room, created_at)
                    VALUES (?, ?, ?)
                    """,
                    (severity, assigned_room, now_text()),
                )
                connection.commit()
                connection.close()
                triage_result = {
                    "severity": severity,
                    "assigned_room": assigned_room,
                }
                form_data = {}

    return render_template(
        "triage.html",
        error_message=error_message,
        triage_result=triage_result,
        form_data=form_data,
    )


@app.route("/staff")
def staff_redirect():
    """Old staff menu link. Send visitors to Home."""
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
