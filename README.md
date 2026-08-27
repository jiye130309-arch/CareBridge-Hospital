# CareBridge Hospital 🏥

A web-based hospital management system developed using **Python Flask, SQLite, HTML, CSS, Docker, Docker Compose, and ngrok**.

CareBridge Hospital modernises traditional hospital management workflows into a web-based application for managing patients, appointments, billing, and triage.

---

## 📌 Project Overview

**CareBridge Hospital** is a Flask-based hospital management web application developed as part of a web migration project.

The application provides staff with a simple interface to perform common hospital management tasks while storing information in a SQLite database.

### Main Features

* 👤 Patient registration
* 📅 Appointment booking
* ✅ Appointment confirmation
* 💰 Patient billing
* 🚑 Triage room assignment
* 🗄️ SQLite database storage
* 🐳 Docker containerisation
* 🌐 ngrok public tunnelling
* 🔐 Input validation

---

## 🛠️ Technologies Used

| Technology         | Purpose                                |
| ------------------ | -------------------------------------- |
| **Python**         | Main programming language              |
| **Flask**          | Web application framework              |
| **SQLite**         | Database management                    |
| **HTML**           | Web page structure                     |
| **CSS**            | User interface styling                 |
| **Docker**         | Application containerisation           |
| **Docker Compose** | Container configuration and management |
| **ngrok**          | Public internet tunnel                 |
| **Git**            | Version control                        |
| **GitHub**         | Source code repository                 |

---

## 📂 Project Structure

```text
CareBridge-Hospital/
│
├── app.py
├── carebridge.db
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
│
├── templates/
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

# 🏥 System Functions

## 1. Register Patient

Staff can register a new patient by entering:

* Patient ID
* Patient name
* Age

The system validates the information before saving the patient record to SQLite.

### Validation

* Patient name cannot be blank
* Patient ID cannot be blank
* Age must be a positive whole number
* Patient IDs must be unique

---

## 2. Book Appointment

Staff can book an appointment for an existing registered patient.

The system requires:

* A registered patient
* Department selection
* Appointment date

### Available Departments

* GP
* Specialist

### Appointment Date Rule

The appointment date must be **at least 8 days from the current date**.

Successful appointments are stored in SQLite with the default status:

```text
Pending
```

After successful booking, the system displays an appointment confirmation page.

---

## 3. Calculate Patient Bill

The billing system calculates the patient's total bill based on:

* Patient type
* Number of laboratory tests
* Consultation fee
* Laboratory test charges
* Subsidised patient discount

### Patient Types

* Subsidised
* Private

The calculated bill is saved into the SQLite database.

---

## 4. Triage Room Assignment

Staff can enter a patient's severity score from **1 to 10**.

The system automatically assigns an appropriate room.

| Severity | Assigned Room |
| -------: | ------------- |
|      1–4 | Waiting Room  |
|      5–7 | Room 1        |
|     8–10 | Room 2        |

The triage record is stored in SQLite.

---

# 🗄️ Database

CareBridge Hospital uses **SQLite** for data storage.

The database file is:

```text
carebridge.db
```

### Database Tables

| Table            | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `patients`       | Stores registered patient information     |
| `appointments`   | Stores appointment information            |
| `bills`          | Stores billing records                    |
| `triage_records` | Stores triage and room assignment records |

The application automatically creates the required tables when it starts.

---

# 🐳 Docker

Docker is used as an **environment standardiser** for the CareBridge Hospital application.

The Docker image is based on:

```text
python:3.12-alpine
```

The application runs inside a Docker container and exposes port **5000**.

---

## Dockerfile

The Dockerfile:

1. Uses Python 3.12 Alpine
2. Sets `/app` as the working directory
3. Installs dependencies from `requirements.txt`
4. Copies the Flask application
5. Copies the HTML templates
6. Copies the static files
7. Starts the Flask application

---

# 🚀 Running with Docker Compose

Docker Compose is the recommended way to run the project.

### 1. Open the project directory

```bash
cd CareBridge-Hospital
```

### 2. Build and start the application

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:5000
```

The current `docker-compose.yml` builds the application image, names the container `carebridge-hospital-container`, exposes port `5000`, and mounts the local `carebridge.db` into the container.

---

## Run in the Background

To start the application in detached mode:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker ps
```

View application logs:

```bash
docker compose logs
```

Stop the application:

```bash
docker compose down
```

---

# 🐳 Running with Docker Directly

Docker Compose is recommended, but the application can also be started manually.

### Build the image

```bash
docker build -t carebridge-hospital .
```

### Run the container

```bash
docker run -p 5000:5000 carebridge-hospital
```

Then open:

```text
http://localhost:5000
```

---

# 🌐 Using ngrok

ngrok is used as a **local internet gateway** to make the locally running CareBridge Hospital application accessible through a public HTTPS URL.

The basic architecture is:

```text
Internet
   │
   ▼
 ngrok
   │
   ▼
Port 5000
   │
   ▼
Docker Container
   │
   ▼
Flask Application
   │
   ▼
SQLite Database
```

---

## 1. Start CareBridge Hospital

Using Docker Compose:

```bash
docker compose up --build
```

Make sure the application is working locally:

```text
http://localhost:5000
```

---

## 2. Start ngrok

Open another PowerShell or Terminal window.

Run:

```bash
ngrok http 5000
```

ngrok will provide a public HTTPS forwarding URL similar to:

```text
https://example.ngrok-free.app
```

Open the generated HTTPS URL to access CareBridge Hospital from another device or network.

> **Note:** A temporary ngrok URL may change when the tunnel is restarted.

---

# 🔄 Complete Deployment Flow

The current project workflow is:

```text
                    ┌─────────────────┐
                    │   Web Browser   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      ngrok      │
                    │ Public HTTPS URL│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Docker Container│
                    │   Port 5000     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Flask / app.py │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     SQLite      │
                    │ carebridge.db   │
                    └─────────────────┘
```

---

# 🔐 Input Validation

The application performs validation before storing information.

Examples include:

* Patient name cannot be blank
* Patient ID cannot be blank
* Age must be a positive whole number
* Duplicate Patient IDs are rejected
* Patient must be registered before booking
* Department must be `GP` or `Specialist`
* Appointment date must be valid
* Appointment date must be at least 8 days from today
* Patient type must be `Subsidised` or `Private`
* Laboratory test quantity must be a whole number
* Triage severity must be between 1 and 10

---

# 💾 Data Persistence with Docker

The project uses a Docker volume mapping for the SQLite database.

```yaml
volumes:
  - ./carebridge.db:/app/carebridge.db
```

This means the database file on the host machine is mounted into the Docker container.

Therefore, restarting the container does not require creating a completely separate database inside the container.

---

# 🧪 Testing the Application

After starting the application, test the main functions:

### Patient Registration

1. Open the registration page
2. Enter a valid Patient ID
3. Enter patient name
4. Enter age
5. Submit the form
6. Confirm that the patient is registered

### Appointment Booking

1. Select a registered patient
2. Select GP or Specialist
3. Select an appointment date
4. Make sure the date is at least 8 days from today
5. Submit the appointment
6. Check the confirmation page

### Billing

1. Select the patient type
2. Enter the number of laboratory tests
3. Submit the form
4. Check the calculated total

### Triage

1. Enter a severity score from 1–10
2. Submit the form
3. Check the assigned room

---

# 🔧 Git and GitHub

Git is used to track project development.

### Check project status

```bash
git status
```

### Add changes

```bash
git add .
```

### Commit changes

```bash
git commit -m "Update CareBridge Hospital"
```

### Push to GitHub

```bash
git push origin main
```

---

# 📋 Requirements

### For local Python development

* Python 3.x
* Flask
* SQLite
* Git

### For containerised deployment

* Docker Desktop
* Docker Compose

### For public access

* ngrok

---

# ⚠️ Important Notes

* This project is intended for educational and demonstration purposes.
* Do not enter real patient or sensitive medical information.
* The SQLite database is intended for project/demo use.
* The ngrok URL may change when a temporary tunnel is restarted.
* Docker Desktop must be running before using Docker commands.
* Port `5000` must be available.
* Make sure the Flask application is configured to listen on the Docker-accessible interface and port.

---

# 👨‍💻 Project Information

| Item                     | Details                             |
| ------------------------ | ----------------------------------- |
| **Project**              | CareBridge Hospital                 |
| **Application**          | Hospital Management Web Application |
| **Framework**            | Flask                               |
| **Programming Language** | Python                              |
| **Database**             | SQLite                              |
| **Containerisation**     | Docker                              |
| **Container Management** | Docker Compose                      |
| **Public Tunnel**        | ngrok                               |
| **Version Control**      | Git                                 |
| **Repository Hosting**   | GitHub                              |

---

## 🔗 GitHub Repository

[CareBridge Hospital – GitHub](https://github.com/jiye130309-arch/CareBridge-Hospital)

---

## 📌 Quick Start

The fastest way to run the current version:

```bash
docker compose up --build
```

Open:

```text
http://localhost:5000
```

Then, in another terminal:

```bash
ngrok http 5000
```

Use the HTTPS URL provided by ngrok for external access.

---

**CareBridge Hospital — Modernising Hospital Management Through Web Technology.**
