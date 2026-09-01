# 🏥 CareBridge Hospital

> A containerised web-based hospital management system developed with Python Flask and SQLite to digitalise core hospital workflows including patient registration, appointments, billing, and triage.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Enabled-2496ED?logo=docker\&logoColor=white)](https://docs.docker.com/compose/)
[![ngrok](https://img.shields.io/badge/ngrok-Public%20HTTPS-1F1E37?logo=ngrok\&logoColor=white)](https://ngrok.com/)

---

## 📖 Overview

**CareBridge Hospital** is a Flask-based hospital management web application created as part of a web migration project.

The system transforms common hospital workflows into a centralised web application, allowing staff to manage patient information, appointments, billing, and triage through a browser-based interface.

The application uses **SQLite** for persistent data storage and is containerised using **Docker** and **Docker Compose**. **ngrok** can be used to expose the local application through a public HTTPS URL for demonstrations and remote access.

---

## ✨ Features

### 👤 Patient Registration

Register and store patient information including:

* Patient ID
* Patient name
* Age

The system validates the submitted information and prevents duplicate patient IDs.

### 📅 Appointment Management

Staff can create appointments for registered patients.

The appointment workflow includes:

* Patient selection
* Department selection
* Appointment date selection
* Appointment validation
* Appointment confirmation
* Appointment status tracking

Supported departments include:

* General Medicine
* Cardiology
* Pediatrics
* Orthopedics
* Emergency Medicine
* Diagnostic Medicine

Appointments are initially assigned a **Pending** status.

### 🕐 Appointment Date Validation

Appointments must be scheduled **more than 7 days from the current date**.

This prevents appointments from being created within the restricted booking period.

### 💰 Billing

The billing module calculates patient charges based on the selected billing information.

The system supports:

* Patient type
* Consultation charges
* Laboratory test charges
* Applicable subsidies

Billing information is stored in the SQLite database.

### 🚑 Triage

The triage module records a patient's severity score and assigns an appropriate room.

Severity levels range from **1 to 10**.

| Severity | Assigned Room |
| -------: | ------------- |
|      1–4 | Waiting Room  |
|      5–7 | Room 1        |
|     8–10 | Room 2        |

---

# 🛠️ Technology Stack

| Technology     | Role                         |
| -------------- | ---------------------------- |
| Python 3.12    | Backend programming language |
| Flask          | Web application framework    |
| SQLite         | Database                     |
| HTML           | Page structure               |
| CSS            | User interface               |
| JavaScript     | Client-side functionality    |
| Docker         | Application containerisation |
| Docker Compose | Container management         |
| ngrok          | Public HTTPS tunnelling      |
| Git            | Version control              |
| GitHub         | Source code hosting          |

---

# 🏗️ System Architecture

```text
                         ┌───────────────────┐
                         │     Web Browser   │
                         └─────────┬─────────┘
                                   │
                                   │ HTTPS
                                   ▼
                         ┌───────────────────┐
                         │       ngrok       │
                         │  Public HTTPS URL │
                         └─────────┬─────────┘
                                   │
                                   │ HTTP
                                   ▼
                         ┌───────────────────┐
                         │  localhost:5000   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  Docker Compose   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ CareBridge Docker  │
                         │     Container     │
                         └─────────┬─────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                  ┌─────────────┐     ┌─────────────┐
                  │    Flask    │     │    SQLite   │
                  │   app.py    │     │carebridge.db│
                  └─────────────┘     └─────────────┘
```

---

# 📂 Project Structure

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

# 🚀 Getting Started

## Prerequisites

Install the following before running the project:

* Python 3.12+
* Docker Desktop
* Docker Compose
* Git
* ngrok

Make sure **Docker Desktop is running** before starting the application with Docker Compose.

---

# 📥 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/jiye130309-arch/CareBridge-Hospital.git
```

Move into the project directory:

```bash
cd CareBridge-Hospital
```

---

# 🐳 Running with Docker

Docker Compose is the recommended method for running CareBridge Hospital.

## 2. Build and Start

```powershell
docker compose up --build -d
```

This command:

1. Builds the Docker image.
2. Installs the Python dependencies.
3. Copies the Flask application and frontend files.
4. Creates the CareBridge container.
5. Starts the application in the background.

---

## 3. Check the Container

```powershell
docker compose ps
```

The CareBridge container should be running.

---

## 4. Open the Application

Open a browser and visit:

```text
http://localhost:5000
```

---

# 🐳 Dockerfile

CareBridge Hospital uses the following Dockerfile:

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

CMD ["python", "app.py"]
```

### Dockerfile Explanation

| Instruction               | Purpose                                         |
| ------------------------- | ----------------------------------------------- |
| `FROM python:3.12-alpine` | Uses Python 3.12 with Alpine Linux              |
| `WORKDIR /app`            | Sets the working directory inside the container |
| `COPY requirements.txt .` | Copies the dependency file                      |
| `RUN pip install ...`     | Installs the required Python packages           |
| `COPY app.py .`           | Copies the Flask application                    |
| `COPY templates/`         | Copies the HTML templates                       |
| `COPY static/`            | Copies CSS, JavaScript and static assets        |
| `CMD`                     | Starts the Flask application                    |

The Dockerfile does not need to copy the SQLite database because the database is mounted through Docker Compose.

---

# 📦 Docker Compose

The project uses `docker-compose.yml` to configure and run the CareBridge container.

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

| Configuration                        | Purpose                                        |
| ------------------------------------ | ---------------------------------------------- |
| `build: .`                           | Builds the image from the Dockerfile           |
| `container_name`                     | Sets the container name                        |
| `5000:5000`                          | Maps host port 5000 to container port 5000     |
| `./carebridge.db:/app/carebridge.db` | Mounts the SQLite database                     |
| `restart: unless-stopped`            | Restarts the container unless manually stopped |

---

# 💾 Database Persistence

CareBridge Hospital uses SQLite.

The primary database file is:

```text
carebridge.db
```

The project also includes:

```text
carebridge.sql
```

The database is mounted into the Docker container using:

```yaml
volumes:
  - ./carebridge.db:/app/carebridge.db
```

This allows database records to remain available when the Docker container is stopped or recreated.

---

# 🌐 Public Access with ngrok

ngrok allows CareBridge Hospital to be accessed through a public HTTPS URL.

First, make sure the application is running:

```powershell
docker compose up --build -d
```

Test the local application:

```text
http://localhost:5000
```

Once the local application is working, open a **second PowerShell window**.

Run:

```powershell
ngrok http 5000
```

ngrok will display a forwarding address similar to:

```text
Forwarding
https://example.ngrok-free.app -> http://localhost:5000
```

Open the HTTPS URL in a browser to access CareBridge Hospital.

---

# 🔑 ngrok Authentication

If your ngrok authentication token has not been configured, run:

```powershell
ngrok config add-authtoken "YOUR_NGROK_AUTHTOKEN"
```

Verify the configuration:

```powershell
ngrok config check
```

> **Security:** Never commit your real ngrok authentication token to GitHub or include it in this README.

---

# 🔄 Complete Startup Workflow

For a normal project demonstration, use two PowerShell windows.

## Terminal 1 — Docker

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"

docker compose up --build -d

docker compose ps
```

Then open:

```text
http://localhost:5000
```

---

## Terminal 2 — ngrok

```powershell
ngrok http 5000
```

Copy the HTTPS forwarding URL provided by ngrok.

Example:

```text
https://example.ngrok-free.app
```

---

# 🧪 Testing

## Patient Registration

1. Open the patient registration page.
2. Enter a valid Patient ID.
3. Enter the patient's name.
4. Enter the patient's age.
5. Submit the form.
6. Confirm that the patient is registered.
7. Verify the record in the database.

## Appointment Booking

1. Select a registered patient.
2. Select a department.
3. Select an appointment date.
4. Ensure the date is more than 7 days from today.
5. Submit the appointment.
6. Verify the confirmation page.
7. Confirm the appointment status.

## Billing

1. Select the patient.
2. Enter the required billing information.
3. Submit the billing form.
4. Verify the calculated bill.
5. Confirm the billing record.

## Triage

1. Enter a severity score from 1 to 10.
2. Submit the triage form.
3. Verify the assigned room.
4. Confirm the triage record.

---

# 🔐 Validation

The application performs validation before processing submitted data.

### Patient Registration

* Patient ID cannot be empty.
* Patient name cannot be empty.
* Age must be valid.
* Duplicate Patient IDs are prevented.

### Appointment Booking

* Patient must be registered.
* Department must be valid.
* Appointment date must be valid.
* Appointment date must be more than 7 days from today.

### Billing

* Patient type must be valid.
* Laboratory test quantity must be valid.

### Triage

* Severity must be a valid integer.
* Severity must be between 1 and 10.

---

# 🧰 Useful Docker Commands

### Start

```powershell
docker compose up --build -d
```

### Stop

```powershell
docker compose down
```

### Restart

```powershell
docker compose restart
```

### Check containers

```powershell
docker compose ps
```

### View logs

```powershell
docker compose logs
```

### Follow logs

```powershell
docker compose logs -f
```

### Rebuild

```powershell
docker compose down
docker compose up --build -d
```

---

# 🔧 Troubleshooting

## Flask is not installed

If running the application directly with Python produces:

```text
ModuleNotFoundError: No module named 'flask'
```

install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

For the recommended setup, use Docker Compose instead:

```powershell
docker compose up --build -d
```

---

## Docker is not recognised

Check:

```powershell
docker --version
```

If Docker is not recognised, install Docker Desktop and ensure it is running.

---

## Container is not running

Check:

```powershell
docker compose ps
```

View the logs:

```powershell
docker compose logs
```

Then rebuild:

```powershell
docker compose down
docker compose up --build -d
```

---

## Website is not updating

Rebuild the Docker image:

```powershell
docker compose down
docker compose up --build -d
```

Then refresh:

```text
http://localhost:5000
```

If the problem continues, check:

```powershell
docker compose logs -f
```

---

## ngrok is not recognised

Check:

```powershell
ngrok version
```

If PowerShell cannot find ngrok, make sure ngrok is installed and its executable directory is included in the Windows PATH.

After updating PATH, close PowerShell and open a new PowerShell window.

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

First verify that CareBridge works locally:

```text
http://localhost:5000
```

Then check:

```powershell
docker compose ps
```

If the container is stopped:

```powershell
docker compose up --build -d
```

Then start:

```powershell
ngrok http 5000
```

---

# 🔀 Git Workflow

The project uses Git for version control and GitHub for repository hosting.

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

### Pull latest changes

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

# 🔒 Security Considerations

CareBridge Hospital is an **educational project** and is not intended for production healthcare use.

For demonstrations:

* Do not enter real patient information.
* Do not store real medical records.
* Do not expose sensitive information through ngrok.
* Keep authentication tokens private.
* Never commit credentials to GitHub.
* Do not share your ngrok authentication token.
* SQLite is intended for this project's development and demonstration requirements.

A production healthcare system would require additional security controls, authentication, authorisation, encryption, auditing, secure infrastructure, and compliance with applicable healthcare regulations.

---

# 🚧 Future Improvements

Potential future enhancements include:

* User authentication
* Role-based access control
* Doctor and staff accounts
* Advanced appointment scheduling
* Appointment notifications
* Patient search
* Medical record management
* Dashboard analytics
* Audit logging
* REST API
* Automated testing
* CI/CD integration
* Cloud deployment
* PostgreSQL or another production database
* Improved security and access control

---

# 🤖 AI-Assisted Development

AI tools were used as learning and development assistants during the project.

AI assistance supported areas including:

* Python and Flask development
* SQLite database development
* HTML and CSS
* JavaScript
* Docker
* Docker Compose
* ngrok configuration
* Git and GitHub troubleshooting
* Input validation
* Appointment date validation
* Documentation
* Project presentation preparation

AI was used to support the development and learning process. The application was implemented, tested, and reviewed as part of the project.

---

# 📊 Project Information

| Property         | Details                             |
| ---------------- | ----------------------------------- |
| Project          | CareBridge Hospital                 |
| Project Type     | Hospital Management Web Application |
| Backend          | Python / Flask                      |
| Frontend         | HTML / CSS / JavaScript             |
| Database         | SQLite                              |
| Containerisation | Docker                              |
| Orchestration    | Docker Compose                      |
| Public Access    | ngrok                               |
| Version Control  | Git                                 |
| Repository       | GitHub                              |
| Application Port | `5000`                              |

---

# 🔗 Repository

**GitHub Repository**

https://github.com/jiye130309-arch/CareBridge-Hospital

---

# ⚠️ Disclaimer

CareBridge Hospital is developed for **educational and demonstration purposes only**.

This application is not intended to be used as a production hospital information system and must not be used to process real patient, medical, or other sensitive healthcare information.

---

<div align="center">

### 🏥 CareBridge Hospital

**Digitalising Hospital Management Through Web Technology**

</div>
