-- CareBridge Hospital SQLite schema
-- Tables: patients, appointments, bills, triage_records

CREATE TABLE "appointments" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        );

CREATE TABLE bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_type TEXT NOT NULL,
            lab_tests INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL
        );

CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

CREATE TABLE triage_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity INTEGER NOT NULL,
            assigned_room TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

CREATE TRIGGER trg_patient_gone_on_appt_completed_insert
        AFTER INSERT ON appointments
        WHEN upper(trim(replace(replace(NEW.status, char(160), ' '), char(9), ' '))) IN ('COMPLETED', 'COMPLETE')
        BEGIN
            DELETE FROM patients
            WHERE (
                trim(coalesce(NEW.patient_code, '')) != ''
                AND upper(trim(patient_code)) = upper(trim(NEW.patient_code))
            )
            OR upper(trim(name)) = upper(trim(NEW.full_name));
        END;

CREATE TRIGGER trg_patient_gone_on_appt_completed_update
        AFTER UPDATE ON appointments
        WHEN upper(trim(replace(replace(NEW.status, char(160), ' '), char(9), ' '))) IN ('COMPLETED', 'COMPLETE')
        BEGIN
            DELETE FROM patients
            WHERE (
                trim(coalesce(NEW.patient_code, '')) != ''
                AND upper(trim(patient_code)) = upper(trim(NEW.patient_code))
            )
            OR upper(trim(name)) = upper(trim(NEW.full_name));
        END;
