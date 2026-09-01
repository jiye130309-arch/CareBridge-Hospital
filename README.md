# CareBridge Hospital

> A containerised web-based hospital management system built with Flask and SQLite, providing digital workflows for patient registration, appointment management, billing, and triage.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Enabled-2496ED?logo=docker\&logoColor=white)](https://docs.docker.com/compose/)
[![ngrok](https://img.shields.io/badge/ngrok-Public%20Tunnel-1F1E37?logo=ngrok\&logoColor=white)](https://ngrok.com/)

---

## Overview

**CareBridge Hospital** is a Flask-based hospital management application designed to demonstrate the migration of traditional hospital workflows into a centralised web application.

The system provides a structured interface for hospital staff to manage core operational processes while using SQLite for persistent data storage.

The application is containerised with Docker and Docker Compose, while **ngrok** can be used to expose the local application through a public HTTPS endpoint for demonstrations and remote testing.

### Core capabilities

* Patient registration and management
* Appointment booking and validation
* Appointment status management
* Patient billing
* Triage and room assignment
* SQLite database persistence
* Input validation
* Docker containerisation
* Docker Compose orchestration
* Public HTTPS access through ngrok

---

## Features

### Patient Management

Staff can register patients with essential information including:

* Patient ID
* Patient name
* Age

The system validates patient information before storing it in the database and prevents duplicate patient IDs.

### Appointment Management

Staff can create appointments for registered patients.

The appointment workflow includes:

* Patient selection
* Department selection
* Appointment date validation
* Appointment confirmation
* Appointment status tracking

Supported departments:

* General Medicine
* Cardiology
* Pediatrics
* Orthopedics
* Emergency Medicine
* Diagnostic Medicine

Appointments are initially assigned a **Pending** status.

### Appointment Date Validation

The application validates appointment dates before accepting a booking.

Appointments must be scheduled **more than 7 days from the current date**.

This validation helps prevent appointments from being created within the restricted booking period.

### Billing

The billing module calculates patient charges based on:

* Patient type
* Consultation fees
* Laboratory tests
* Applicable charges or subsidies

Billing records are stored in SQLite for persistence.

### Triage

The triage module records a patient's severity level and assigns an appropriate room.

Severity scores range from **1 to 10**.

| Severity | Assignment   |
| -------: | ------------ |
|      1–4 | Waiting Room |
|      5–7 | Room 1       |
|     8–10 | Room 2       |

---

## Technology Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Backend          | Python / Flask          |
| Frontend         | HTML / CSS / JavaScript |
| Database         | SQLite                  |
| Containerisation | Docker                  |
| Orchestration    | Docker Compose          |
| Public Access    | ngrok                   |
| Version Control  | Git                     |
| Repository       | GitHub                  |

---

## Architecture

```text
                         ┌──────────────────────┐
                         │      Web Browser     │
                         └──────────┬───────────┘
                                    │
                                    │ HTTPS
                                    ▼
                         ┌──────────────────────┐
                         │        ngrok         │
                         │   Public HTTPS URL   │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │     Docker Host      │
                         │     Port :5000       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   CareBridge Flask   │
                         │      Container       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       SQLite         │
                         │    carebridge.db     │
                         └──────────────────────┘
```

### Request flow

```text
Browser
   ↓
ngrok
   ↓
localhost:5000
   ↓
Docker Compose
   ↓
Flask
   ↓
SQLite
```

---

## Project Structure

```text
CareBridge-Hospital/
│
├── app.py
├── carebridge.db
├── carebridge.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── services.html
│   ├── doctors.html
│   ├── register.html
│   ├── appointments.html
│   ├── appointment_confirmation.html
│   ├── bill.html
│   └── ...
│
└── static/
    ├── css/
    │   └── style.css
    └── ...
```

---

# Getting Started

## Prerequisites

Before running CareBridge Hospital, install:

* Python 3.12 or later
* Docker Desktop
* Git
* ngrok

Docker Desktop should be running before starting the containerised application.

---

## Clone the Repository

```bash
git clone https://github.com/jiye130309-arch/CareBridge-Hospital.git
cd CareBridge-Hospital
```

---

# Running with Docker Compose

Docker Compose is the recommended method for running the application.

## Start the application

```powershell
docker compose up --build -d
```

The application will be available locally at:

```text
http://localhost:5000
```

## Check container status

```powershell
docker compose ps
```

## View logs

```powershell
docker compose logs -f
```

## Restart the application

```powershell
docker compose restart
```

## Stop the application

```powershell
docker compose down
```

---

# Docker Configuration

The project uses a `Dockerfile` to create the application image and `docker-compose.yml` to manage the container.

### Dockerfile

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Docker Compose

```yaml
services:
  carebridge:
    build: .
    container_name: carebridge-hospital
    ports:
      - "5000:5000"
    volumes:
      - ./carebridge.db:/app/carebridge.db
    restart: unless-stopped
```

### Configuration

| Setting                              | Description                                  |
| ------------------------------------ | -------------------------------------------- |
| `build: .`                           | Builds the image from the project Dockerfile |
| `container_name`                     | Sets the Docker container name               |
| `5000:5000`                          | Maps host port 5000 to container port 5000   |
| `./carebridge.db:/app/carebridge.db` | Persists SQLite data                         |
| `restart: unless-stopped`            | Automatically restarts the container         |

---

# Database

CareBridge Hospital uses **SQLite** as its database engine.

### Database file

```text
carebridge.db
```

### SQL file

```text
carebridge.sql
```

The database is used to persist application records across sessions.

### Main data areas

| Data         | Purpose                              |
| ------------ | ------------------------------------ |
| Patients     | Patient registration and information |
| Appointments | Appointment records and statuses     |
| Billing      | Patient billing information          |
| Triage       | Severity and room assignment         |

The Docker Compose volume ensures that the SQLite database remains available when the container is recreated.

---

# ngrok Public Access

ngrok allows the locally running application to be accessed through a public HTTPS URL.

First, make sure CareBridge is running:

```powershell
docker compose up --build -d
```

Verify locally:

```text
http://localhost:5000
```

Then open a **second PowerShell window** and run:

```powershell
ngrok http 5000
```

ngrok will provide a forwarding address similar to:

```text
https://example.ngrok-free.app
```

Open the HTTPS address in a browser to access the application remotely.

### ngrok workflow

```text
Local CareBridge
      │
      │ localhost:5000
      ▼
    ngrok
      │
      │ HTTPS
      ▼
Public Internet
```

> **Note:** The free ngrok URL is normally temporary and may change when the tunnel is restarted.

---

# ngrok Authentication

If authentication has not been configured, add your ngrok authentication token:

```powershell
ngrok config add-authtoken "YOUR_NGROK_AUTHTOKEN"
```

Verify the configuration:

```powershell
ngrok config check
```

### Security

Never commit your actual authentication token to GitHub.

Do not place it inside:

* `README.md`
* `app.py`
* `docker-compose.yml`
* `.env` files that are committed
* Git commits
* Screenshots shared publicly

---

# Local Development

Docker Compose is recommended for normal project execution.

If you want to run Flask directly on the host machine, first install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Then:

```powershell
python app.py
```

The application should be available at:

```text
http://localhost:5000
```

### Recommended workflow

For demonstrations:

```text
Docker Compose
     ↓
Flask Container
     ↓
localhost:5000
     ↓
ngrok
     ↓
Public HTTPS URL
```

---

# Validation

CareBridge Hospital includes validation logic for the main workflows.

### Patient validation

* Patient ID cannot be empty
* Patient name cannot be empty
* Age must be valid
* Duplicate patient IDs are prevented

### Appointment validation

* Patient must exist
* Department must be valid
* Appointment date must be valid
* Appointment must be more than 7 days from the current date

### Billing validation

* Patient type must be valid
* Laboratory test quantity must be valid

### Triage validation

* Severity must be an integer
* Severity must be between 1 and 10

---

# Testing

The application should be tested using the following workflow.

## Patient Registration

1. Navigate to patient registration.
2. Enter valid patient information.
3. Submit the form.
4. Verify successful registration.
5. Confirm the record is stored in SQLite.

## Appointment Booking

1. Select a registered patient.
2. Select a department.
3. Select a valid appointment date.
4. Submit the appointment.
5. Verify the confirmation page.
6. Confirm the appointment is stored with the correct status.

## Billing

1. Select the patient.
2. Enter the required billing information.
3. Submit the form.
4. Verify the calculated total.
5. Confirm the billing record is stored.

## Triage

1. Enter a severity score.
2. Submit the triage form.
3. Verify the assigned room.
4. Confirm the record is stored.

---

# Troubleshooting

## Flask module not found

If you run:

```powershell
python app.py
```

and receive:

```text
ModuleNotFoundError: No module named 'flask'
```

install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Alternatively, use Docker Compose:

```powershell
docker compose up --build -d
```

---

## Docker is not recognised

Check:

```powershell
docker --version
```

If Docker is not recognised, ensure Docker Desktop is installed and running.

---

## Container is not running

Check:

```powershell
docker compose ps
```

Then inspect the logs:

```powershell
docker compose logs
```

Rebuild if necessary:

```powershell
docker compose down
docker compose up --build -d
```

---

## Website changes are not appearing

Rebuild the Docker image:

```powershell
docker compose down
docker compose up --build -d
```

Then refresh:

```text
http://localhost:5000
```

You can also monitor the application:

```powershell
docker compose logs -f
```

---

## ngrok is not recognised

Check:

```powershell
ngrok version
```

If the command is not recognised, ensure the ngrok executable directory has been added to the Windows PATH.

After updating PATH, close and reopen PowerShell.

Then run:

```powershell
ngrok version
```

Once recognised:

```powershell
ngrok http 5000
```

---

## ngrok cannot connect

First verify that the application works locally:

```text
http://localhost:5000
```

Then check Docker:

```powershell
docker compose ps
```

If the container is stopped:

```powershell
docker compose up --build -d
```

Finally:

```powershell
ngrok http 5000
```

---

# Git Workflow

The project uses Git for version control.

### Check status

```powershell
git status
```

### Stage changes

```powershell
git add .
```

### Commit changes

```powershell
git commit -m "Update CareBridge Hospital"
```

### Pull the latest version

```powershell
git pull --rebase origin main
```

### Push changes

```powershell
git push origin main
```

### Recommended workflow

```text
Modify
  ↓
Test
  ↓
git status
  ↓
git add .
  ↓
git commit
  ↓
git pull --rebase
  ↓
git push
```

---

# Security Considerations

CareBridge Hospital is an **educational project** and should not be used for real clinical operations.

For demonstration purposes:

* Do not enter real patient information.
* Do not store real medical records.
* Do not expose sensitive information through ngrok.
* Keep authentication tokens private.
* Do not commit credentials to GitHub.
* Use appropriate authentication and authorisation before production deployment.
* SQLite is suitable for this project but may not be appropriate for a production hospital system.

---

# Future Improvements

Potential future development includes:

* User authentication and role-based access control
* Doctor and staff accounts
* Advanced appointment scheduling
* Email/SMS appointment notifications
* Improved patient search
* Medical record management
* Dashboard analytics
* Audit logging
* REST API integration
* Production-grade database such as PostgreSQL
* Cloud deployment
* Automated testing
* CI/CD pipeline
* Improved security and encryption

---

# Project Workflow

```text
                  ┌─────────────────┐
                  │   Development   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Flask App     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     SQLite      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     Docker      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Docker Compose  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  localhost:5000 │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      ngrok      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Public HTTPS   │
                  └─────────────────┘
```

---

# AI-Assisted Development

AI tools were used as development and learning assistants during the project.

AI assistance was used for areas including:

* Flask development
* Python programming
* SQLite database logic
* HTML and CSS
* JavaScript
* Docker configuration
* Docker Compose
* ngrok configuration
* Git and GitHub troubleshooting
* Input validation
* Appointment date validation
* Documentation
* Project presentation preparation

AI assistance was used to support development and learning. The resulting application was implemented, tested, and reviewed as part of the project.

---

# Project Information

| Property         | Value                               |
| ---------------- | ----------------------------------- |
| Project          | CareBridge Hospital                 |
| Type             | Hospital Management Web Application |
| Backend          | Flask                               |
| Language         | Python                              |
| Database         | SQLite                              |
| Frontend         | HTML / CSS / JavaScript             |
| Containerisation | Docker                              |
| Orchestration    | Docker Compose                      |
| Public Tunnel    | ngrok                               |
| Version Control  | Git                                 |
| Repository       | GitHub                              |
| Application Port | `5000`                              |

---

# Repository

**GitHub:**
https://github.com/jiye130309-arch/CareBridge-Hospital

---

# Educational Disclaimer

CareBridge Hospital is developed for **educational and demonstration purposes**.

It is not intended to replace a production hospital information system and must not be used to process real patient or medical data.

---

## CareBridge Hospital

**Digitalising Hospital Management Through Web Technology.**
