from datetime import date, datetime, timedelta
import sqlite3
#import flask
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = "carebridge.db"

STAFF_DEPARTMENTS = ["GP", "Specialist"]
PATIENT_TYPES = ["Subsidised", "Private"]
ALLOWED_STATUSES = ["Pending", "Confirmed", "Cancelled"]

BASE_CONSULTATION_FEE = 100
LAB_TEST_RATE = 10
SUBSIDY_RATE = 0.70


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
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            department TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
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
    connection.commit()
    connection.close()


def ensure_extra_columns():
    """Add new columns to older databases without replacing existing tables."""
    connection = get_db_connection()
    appointment_columns = get_column_names(connection, "appointments")
    if "status" not in appointment_columns:
        connection.execute(
            "ALTER TABLE appointments ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'"
        )
    if "patient_code" not in appointment_columns:
        connection.execute("ALTER TABLE appointments ADD COLUMN patient_code TEXT")
    connection.commit()
    connection.close()


create_tables()
ensure_extra_columns()


def now_text():
    return datetime.now().isoformat(timespec="seconds")


def min_appointment_date():
    """Appointments must be more than 7 days from today."""
    return date.today() + timedelta(days=8)


def get_patients():
    connection = get_db_connection()
    patients = connection.execute(
        "SELECT id, patient_code, name, age FROM patients ORDER BY name"
    ).fetchall()
    connection.close()
    return patients


def assign_triage_room(severity):
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


@app.route("/register", methods=["GET", "POST"])
def register_patient():
    """Register a patient and save the record in SQLite."""
    error_message = None
    success_message = None
    form_data = {}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        patient_code = request.form.get("patient_code", "").strip()
        form_data = request.form

        if name == "":
            error_message = "Patient name cannot be blank."
        elif patient_code == "":
            error_message = "Patient ID cannot be blank."
        elif not age_text.isdigit() or int(age_text) <= 0:
            error_message = "Age must be a positive whole number."
        else:
            connection = get_db_connection()
            existing = connection.execute(
                "SELECT id FROM patients WHERE patient_code = ?",
                (patient_code,),
            ).fetchone()
            if existing:
                connection.close()
                error_message = "This Patient ID is already registered."
            else:
                connection.execute(
                    """
                    INSERT INTO patients (patient_code, name, age, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (patient_code, name, int(age_text), now_text()),
                )
                connection.commit()
                connection.close()
                success_message = f"Patient {name} ({patient_code}) has been registered."
                form_data = {}

    connection = get_db_connection()
    patients = connection.execute(
        "SELECT patient_code, name, age FROM patients ORDER BY id DESC"
    ).fetchall()
    connection.close()

    return render_template(
        "register_patient.html",
        error_message=error_message,
        success_message=success_message,
        form_data=form_data,
        patients=patients,
    )


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    """Book an appointment for a registered patient."""
    error_message = None
    patients = get_patients()
    earliest_date = min_appointment_date()

    if request.method == "POST":
        patient_code = request.form.get("patient_code", "").strip()
        department = request.form.get("department", "").strip()
        appointment_date_text = request.form.get("appointment_date", "").strip()

        if patient_code == "":
            error_message = "Please select a patient."
        elif department not in STAFF_DEPARTMENTS:
            error_message = "Department must be GP or Specialist."
        else:
            try:
                chosen_date = datetime.strptime(appointment_date_text, "%Y-%m-%d").date()
            except ValueError:
                error_message = "Please enter a valid appointment date."
            else:
                if chosen_date <= date.today() + timedelta(days=7):
                    error_message = "Appointment date must be more than 7 days from today."

        if error_message:
            return render_template(
                "appointments.html",
                departments=STAFF_DEPARTMENTS,
                patients=patients,
                form_data=request.form,
                error_message=error_message,
                min_date=earliest_date.isoformat(),
            )

        connection = get_db_connection()
        patient = connection.execute(
            "SELECT patient_code, name FROM patients WHERE patient_code = ?",
            (patient_code,),
        ).fetchone()
        if patient is None:
            connection.close()
            error_message = "Please select a valid registered patient."
            return render_template(
                "appointments.html",
                departments=STAFF_DEPARTMENTS,
                patients=patients,
                form_data=request.form,
                error_message=error_message,
                min_date=earliest_date.isoformat(),
            )

        cursor = connection.execute(
            """
            INSERT INTO appointments (
                full_name, email, phone, date_of_birth, department, doctor,
                appointment_date, appointment_time, reason, notes, created_at,
                status, patient_code
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient["name"],
                "N/A",
                "N/A",
                "N/A",
                department,
                department,
                appointment_date_text,
                "09:00",
                "Staff booking",
                "",
                now_text(),
                "Pending",
                patient["patient_code"],
            ),
        )
        connection.commit()
        appointment_id = cursor.lastrowid
        connection.close()
        return redirect(url_for("appointment_confirmation", appointment_id=appointment_id))

    return render_template(
        "appointments.html",
        departments=STAFF_DEPARTMENTS,
        patients=patients,
        form_data={},
        error_message=None,
        min_date=earliest_date.isoformat(),
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
        return redirect(url_for("appointments"))

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
            subtotal = BASE_CONSULTATION_FEE + (lab_tests * LAB_TEST_RATE)
            discount = 0
            total = subtotal
            if patient_type == "Subsidised":
                total = subtotal * SUBSIDY_RATE
                discount = subtotal - total

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
def assign_triage():
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
                assigned_room = assign_triage_room(severity)
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
def staff():
    """Show the staff dashboard and saved appointments."""
    connection = get_db_connection()
    appointments = connection.execute(
        """
        SELECT
            id,
            full_name,
            email,
            phone,
            department,
            doctor,
            appointment_date,
            appointment_time,
            reason,
            status,
            patient_code
        FROM appointments
        ORDER BY appointment_date DESC, appointment_time DESC, id DESC
        """
    ).fetchall()
    connection.close()

    return render_template(
        "staff.html",
        appointments=appointments,
        statuses=ALLOWED_STATUSES,
    )


@app.route("/staff/appointment/<int:appointment_id>/status", methods=["POST"])
def update_appointment_status(appointment_id):
    """Update one appointment status, then return to the staff dashboard."""
    new_status = request.form.get("status", "").strip()
    if new_status not in ALLOWED_STATUSES:
        return redirect(url_for("staff"))

    connection = get_db_connection()
    appointment = connection.execute(
        "SELECT id FROM appointments WHERE id = ?",
        (appointment_id,),
    ).fetchone()

    if appointment is None:
        connection.close()
        return redirect(url_for("staff"))

    connection.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        (new_status, appointment_id),
    )
    connection.commit()
    connection.close()
    return redirect(url_for("staff"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
