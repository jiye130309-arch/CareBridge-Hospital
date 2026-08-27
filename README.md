# CareBridge Hospital

A web-based hospital management system developed using **Python Flask, SQLite, HTML, CSS, Docker, and ngrok**.

The project modernises a hospital management workflow by providing a simple web interface for staff to register patients, book appointments, calculate bills, and manage triage information.

---

## 📌 Project Overview

**CareBridge Hospital** is a Flask-based web application designed to demonstrate the migration of a traditional hospital management system into a modern web-based application.

The system provides several hospital management functions:

* Patient registration
* Appointment booking
* Appointment confirmation
* Patient billing
* Triage room assignment
* Staff management interface
* SQLite database storage
* Containerised deployment using Docker
* Internet access/tunnelling using ngrok

---

## 🛠️ Technologies Used

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Main programming language         |
| Flask      | Web application framework         |
| SQLite     | Database management               |
| HTML       | Web page structure                |
| CSS        | User interface styling            |
| Docker     | Application containerisation      |
| ngrok      | Secure tunnel for external access |
| Git        | Version control                   |
| GitHub     | Source code repository            |

---

## 📂 Project Structure

```text
CareBridge-Hospital/
│
├── app.py
├── carebridge.db
├── Dockerfile
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

## 🏥 Main System Functions

### 1. Register Patient

Staff can register a new patient by entering:

* Patient ID
* Patient name
* Age

The system validates the information before storing the patient record in the SQLite database.

Patient IDs must be unique.

---

### 2. Book Appointment

Staff can book an appointment for a registered patient.

The system requires:

* A registered patient
* Department selection
* Appointment date

Available department types:

* GP
* Specialist

The appointment date must be **at least 8 days from the current date**.

Successful appointments are stored in SQLite with a default status of:

```text
Pending
```

The system then displays an appointment confirmation page.

---

### 3. Calculate Patient Bill

The billing function calculates the patient's total bill based on:

* Patient type
* Number of laboratory tests
* Consultation fee
* Laboratory test charges
* Subsidised patient discount

Patient types:

* Subsidised
* Private

The calculated bill is also saved into the SQLite database.

---

### 4. Triage Room Assignment

Staff can enter a patient's severity score from **1 to 10**.

The system assigns the patient to an appropriate room:

| Severity | Assigned Room |
| -------- | ------------- |
| 1–4      | Waiting Room  |
| 5–7      | Room 1        |
| 8–10     | Room 2        |

The triage record is stored in the SQLite database.

---

## 🗄️ Database

The application uses **SQLite** as its database.

The main database file is:

```text
carebridge.db
```

The application contains tables for:

* `patients`
* `appointments`
* `bills`
* `triage_records`

The database is automatically created when the Flask application starts if the required tables do not already exist.

---

# 🐳 Running the Application with Docker

Docker is used to create a consistent environment for running the CareBridge Hospital application.

### 1. Build the Docker image

Open PowerShell or Terminal in the project directory:

```bash
docker build -t carebridge-hospital .
```

### 2. Run the Docker container

```bash
docker run -p 5000:5000 carebridge-hospital
```

The Flask application will then be available locally at:

```text
http://localhost:5000
```

You can also access it using your computer's local IP address if the Docker port is exposed to your network.

Example:

```text
http://192.168.x.x:5000
```

---

# 🌐 Using ngrok

ngrok is used to create a public tunnel to the locally running CareBridge Hospital application.

This allows the application to be accessed from outside the local network.

### 1. Start the Docker container

```bash
docker run -p 5000:5000 carebridge-hospital
```

### 2. Start ngrok

In another terminal:

```bash
ngrok http 5000
```

ngrok will generate a public forwarding address similar to:

```text
https://xxxx-xxxx-xxxx.ngrok-free.app
```

The generated ngrok URL can be shared with others to access the CareBridge Hospital web application.

> **Note:** The ngrok URL may change each time a new temporary tunnel is created.

---

## 🔄 Application Architecture

```text
User
  │
  ▼
Web Browser
  │
  ▼
ngrok
  │
  ▼
Docker Container
  │
  ▼
Flask Application
  │
  ▼
SQLite Database
  │
  ├── Patients
  ├── Appointments
  ├── Bills
  └── Triage Records
```

---

## 🔐 Validation

The application includes input validation to prevent invalid data from being stored.

Examples include:

* Patient name cannot be blank
* Patient ID cannot be blank
* Age must be a positive whole number
* Duplicate Patient IDs are rejected
* Patient must be registered before booking an appointment
* Department must be either GP or Specialist
* Appointment date must be valid
* Appointment date must be at least 8 days from today
* Patient type must be Subsidised or Private
* Number of laboratory tests must be a whole number
* Triage severity must be within the valid range

---

## 🐳 Why Docker?

Docker is used as an **environment standardiser** for the project.

It allows the application and its required environment to be packaged into a container so that it can run consistently across different systems.

Benefits include:

* Consistent Python environment
* Easier application deployment
* Reduced dependency problems
* Portable application environment
* Easier testing and demonstration

---

## 🌐 Why ngrok?

ngrok is used as a **local internet gateway**.

It creates a secure tunnel between the internet and the locally hosted application.

This is useful for:

* Demonstrating the project remotely
* Allowing others to access the application
* Testing the web application from another device
* Presenting the project without deploying it to a permanent cloud server

---

## 🔧 Git and GitHub

Git is used to track changes to the project.

Example commands:

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "Update CareBridge Hospital"
```

```bash
git push origin main
```

The project repository is hosted on GitHub.

---

## ▶️ Quick Start

### Without Docker

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

### With Docker

```bash
docker build -t carebridge-hospital .
```

```bash
docker run -p 5000:5000 carebridge-hospital
```

Then open:

```text
http://localhost:5000
```

### With ngrok

After starting Docker:

```bash
ngrok http 5000
```

Open the HTTPS forwarding URL provided by ngrok.

---

## 📋 Requirements

To run the project locally, you should have:

* Python 3.x
* Flask
* SQLite
* Docker Desktop
* ngrok
* Git

---

## ⚠️ Important Notes

* Do not share sensitive information through the application.
* The SQLite database is intended for project/demo purposes.
* The ngrok URL is temporary when using a temporary tunnel.
* Make sure Docker Desktop is running before building or running the container.
* Make sure the Flask application is listening on the correct host and port inside the Docker container.

---

## 👨‍💻 Project

**Project:** CareBridge Hospital
**Application Type:** Hospital Management Web Application
**Framework:** Flask
**Database:** SQLite
**Containerisation:** Docker
**Internet Gateway:** ngrok
**Version Control:** Git & GitHub
