from datetime import datetime
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

# Flask looks for HTML files in the "templates" folder
# and CSS/JS files in the "static" folder.
app = Flask(__name__)

DATABASE = "carebridge.db"

DEPARTMENTS = [
    "General Medicine",
    "Cardiology",
    "Pediatrics",
    "Orthopedics",
    "Emergency Medicine",
    "Diagnostic Medicine",
]

DOCTORS = [
    "Dr. Sarah Tan",
    "Dr. Michael Lim",
    "Dr. Amanda Lee",
    "Dr. Daniel Wong",
    "Dr. Emily Koh",
    "Dr. Ryan Chen",
]


def get_db_connection():
    """Open the SQLite database used to store appointments."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the appointments table if it does not already exist."""
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
            created_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


create_tables()


@app.route("/")
def home():
    """Show the CareBridge Hospital homepage."""
    return render_template("index.html")


@app.route("/services")
def services():
    """Show the medical services page."""
    return render_template("services.html")


@app.route("/doctors")
def doctors():
    """Show the medical specialists page."""
    return render_template("doctors.html")


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    """Show the booking form, or save a submitted appointment."""
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        date_of_birth = request.form.get("date_of_birth", "").strip()
        department = request.form.get("department", "").strip()
        doctor = request.form.get("doctor", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        reason = request.form.get("reason", "").strip()
        notes = request.form.get("notes", "").strip()

        missing_required = not all(
            [
                full_name,
                email,
                phone,
                date_of_birth,
                department,
                doctor,
                appointment_date,
                appointment_time,
                reason,
            ]
        )
        invalid_choice = department not in DEPARTMENTS or doctor not in DOCTORS

        if missing_required or invalid_choice:
            error_message = "Please complete all required fields and choose a valid department and doctor."
            return render_template(
                "appointments.html",
                departments=DEPARTMENTS,
                doctors=DOCTORS,
                form_data=request.form,
                error_message=error_message,
            )

        connection = get_db_connection()
        cursor = connection.execute(
            """
            INSERT INTO appointments (
                full_name, email, phone, date_of_birth, department, doctor,
                appointment_date, appointment_time, reason, notes, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                phone,
                date_of_birth,
                department,
                doctor,
                appointment_date,
                appointment_time,
                reason,
                notes,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        connection.commit()
        appointment_id = cursor.lastrowid
        connection.close()

        return redirect(url_for("appointment_confirmation", appointment_id=appointment_id))

    return render_template(
        "appointments.html",
        departments=DEPARTMENTS,
        doctors=DOCTORS,
        form_data={},
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
        return redirect(url_for("appointments"))

    return render_template("appointment_confirmation.html", appointment=appointment)


if __name__ == "__main__":
    # host="0.0.0.0" is useful later for Docker.
    # On your computer, open: http://127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
