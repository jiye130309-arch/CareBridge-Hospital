# 🏥 CareBridge Hospital

A web-based hospital management system developed using **Python Flask, SQLite, HTML, CSS, Docker, Docker Compose, Git, GitHub, and ngrok**.

CareBridge Hospital modernises traditional hospital management workflows into a web-based application that allows hospital staff to manage **patients, appointments, billing, and triage** through a simple interface.

> **Project Type:** Educational / Web Migration Project
> **Application:** Hospital Management Web Application
> **Framework:** Flask
> **Database:** SQLite
> **Containerisation:** Docker
> **Public Access:** ngrok

---

## 📌 Project Overview

**CareBridge Hospital** is a Flask-based hospital management web application developed as part of a web migration project.

The system provides hospital staff with a simple web interface for performing common hospital management tasks while storing records in a SQLite database.

### Main Features

* 👤 Patient registration
* 📅 Appointment booking
* ✅ Appointment confirmation
* 💰 Patient billing
* 🚑 Triage room assignment
* 🗄️ SQLite database storage
* 🐳 Docker containerisation
* 📦 Docker Compose
* 🌐 ngrok public tunnelling
* 🔐 Input validation
* 💾 Persistent database storage

---

# 🛠️ Technologies Used

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

# 📂 Project Structure

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

## 1. 👤 Register Patient

Hospital staff can register a new patient by entering:

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

## 2. 📅 Book Appointment

Staff can book an appointment for an existing registered patient.

The system requires:

* A registered patient
* Department selection
* Appointment date

### Available Departments

* **GP**
* **Specialist**

### Appointment Date Rule

The appointment date must be **at least 8 days from the current date**.

This means:

```text
Today
  ↓
Next 7 days → Not selectable
  ↓
8th day onward → Selectable
```

Successful appointments are stored in SQLite with the default status:

```text
Pending
```

After successful booking, the system displays an appointment confirmation page.

---

## 3. 💰 Calculate Patient Bill

The billing system calculates the patient's total bill based on:

* Patient type
* Consultation fee
* Number of laboratory tests
* Laboratory test charges
* Subsidised patient discount

### Patient Types

* **Subsidised**
* **Private**

The calculated bill is saved into the SQLite database.

---

## 4. 🚑 Triage Room Assignment

Staff can enter a patient's severity score from **1 to 10**.

The system automatically assigns an appropriate room based on the severity level.

| Severity | Assigned Room |
| -------: | ------------- |
|  **1–4** | Waiting Room  |
|  **5–7** | Room 1        |
| **8–10** | Room 2        |

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

The application automatically creates the required database tables when it starts.

---

# 🔐 Input Validation

The application validates user input before storing information.

### Patient Registration

* Patient name cannot be blank
* Patient ID cannot be blank
* Age must be a positive whole number
* Duplicate Patient IDs are rejected

### Appointment Booking

* Patient must already be registered
* Department must be `GP` or `Specialist`
* Appointment date must be valid
* Appointment date must be at least 8 days from today

### Billing

* Patient type must be `Subsidised` or `Private`
* Laboratory test quantity must be a whole number

### Triage

* Severity must be a whole number
* Severity must be between `1` and `10`

---

# 🐳 Docker

Docker is used as an **environment standardiser** for the CareBridge Hospital application.

The Docker image is based on:

```text
python:3.12-alpine
```

The application runs inside a Docker container and uses **port 5000**.

### Why Docker?

Docker helps the project by providing:

* Consistent development environment
* Dependency management
* Application isolation
* Reproducible setup
* Easier deployment
* Easier project demonstration

---

# 🐳 Dockerfile

The Dockerfile is responsible for creating the CareBridge Hospital container environment.

A simplified version of the Dockerfile is:

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 5000

CMD ["python", "app.py"]
```

### Dockerfile Instructions

| Instruction | Purpose                             |
| ----------- | ----------------------------------- |
| `FROM`      | Selects the Python base image       |
| `WORKDIR`   | Sets the working directory          |
| `COPY`      | Copies project files into the image |
| `RUN`       | Installs project dependencies       |
| `EXPOSE`    | Documents the application port      |
| `CMD`       | Starts the Flask application        |

---

# 🚀 Running with Docker Compose

Docker Compose is the recommended way to run CareBridge Hospital.

## 1. Open the project directory

PowerShell:

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"
```

If the repository was cloned into another directory, use that directory instead.

---

## 2. Build and start the application

```powershell
docker compose up --build
```

The application will be available at:

```text
http://localhost:5000
```

---

## 3. Run in the background

To start the application in detached mode:

```powershell
docker compose up --build -d
```

---

## 4. Check the container

```powershell
docker compose ps
```

You should see the CareBridge container running and port `5000` mapped.

Example:

```text
carebridge-hospital-container
0.0.0.0:5000->5000/tcp
```

---

## 5. View application logs

```powershell
docker compose logs
```

To continuously follow the logs:

```powershell
docker compose logs -f
```

---

## 6. Stop the application

```powershell
docker compose down
```

---

# 🐳 Running with Docker Directly

Docker Compose is recommended, but the application can also be started manually.

## Build the Docker image

```powershell
docker build -t carebridge-hospital .
```

## Run the container

```powershell
docker run -p 5000:5000 carebridge-hospital
```

Then open:

```text
http://localhost:5000
```

---

# 💾 SQLite Database Persistence

The project uses a Docker volume mapping for the SQLite database.

The `docker-compose.yml` contains a database mapping similar to:

```yaml
volumes:
  - ./carebridge.db:/app/carebridge.db
```

This maps the SQLite database on the host machine to the database location inside the Docker container.

### Why this is important

Without persistent storage, data stored only inside a container could be lost when the container is removed.

The volume mapping allows the project to continue using the host's:

```text
carebridge.db
```

when the Docker container is restarted.

---

# 🌐 Using ngrok

ngrok is used as a **local internet gateway** to make the locally running CareBridge Hospital application accessible through a public HTTPS URL.

The CareBridge application runs on **port 5000**.

The basic architecture is:

```text
Internet
   │
   ▼
 ngrok Public HTTPS URL
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

# 🌐 ngrok Setup

## 1. Start CareBridge Hospital

Open PowerShell:

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"
```

Start Docker Compose:

```powershell
docker compose up -d
```

Check that the container is running:

```powershell
docker compose ps
```

Then test the local application:

```text
http://localhost:5000
```

Make sure CareBridge Hospital works locally before starting ngrok.

---

# 2. Locate the ngrok Executable

Because ngrok is installed through the **Microsoft Store**, the executable may not be directly available through the normal PowerShell `PATH`.

Run:

```powershell
$pkg = Get-AppxPackage ngrok.ngrok
```

Then locate `ngrok.exe`:

```powershell
$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
```

This stores the location of the ngrok executable in:

```text
$ngrokExe
```

---

# 3. Start the ngrok Tunnel

Run:

```powershell
& "$ngrokExe" http 5000
```

ngrok will create a public HTTPS forwarding URL.

Example:

```text
Forwarding
https://xxxx.ngrok-free.dev -> http://localhost:5000
```

Copy the HTTPS URL and open it in a browser.

The public URL can also be opened from another device.

---

# ⚡ Quick ngrok Command

If `$ngrokExe` has already been defined in the current PowerShell session, you only need:

```powershell
& "$ngrokExe" http 5000
```

If PowerShell has been closed, define the executable path again:

```powershell
$pkg = Get-AppxPackage ngrok.ngrok

$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
```

Then:

```powershell
& "$ngrokExe" http 5000
```

---

# 🔄 Complete Startup Sequence

The normal CareBridge demonstration workflow is:

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"

docker compose up -d

docker compose ps

$pkg = Get-AppxPackage ngrok.ngrok

$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName

& "$ngrokExe" http 5000
```

After ngrok starts, look for:

```text
Forwarding
```

Then copy the generated:

```text
https://xxxx.ngrok-free.dev
```

address.

---

# 🔄 Complete System Workflow

The overall CareBridge Hospital workflow is:

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
                    │    Port 5000    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flask / app.py  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     SQLite      │
                    │  carebridge.db  │
                    └─────────────────┘
```

---

# 🔧 Git & GitHub

Git is used to track project development and GitHub is used as the remote repository.

## Check project status

```powershell
git status
```

## Add changes

```powershell
git add .
```

## Commit changes

```powershell
git commit -m "Update CareBridge Hospital"
```

## Pull changes

```powershell
git pull --rebase origin main
```

## Push changes to GitHub

```powershell
git push origin main
```

---

# 📋 Common Git Workflow

```text
Edit Code
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
    ↓
GitHub
```

---

# 🧪 Testing the Application

After starting CareBridge Hospital, test each major function.

## Patient Registration

1. Open the registration page.
2. Enter a valid Patient ID.
3. Enter the patient's name.
4. Enter the patient's age.
5. Submit the form.
6. Confirm that the patient is registered.
7. Verify that the information is stored in SQLite.

---

## Appointment Booking

1. Select an existing registered patient.
2. Select `GP` or `Specialist`.
3. Select an appointment date.
4. Make sure the appointment is at least **8 days from today**.
5. Submit the appointment.
6. Check the appointment confirmation page.
7. Verify that the appointment status is `Pending`.

---

## Billing

1. Select the patient type.
2. Enter the number of laboratory tests.
3. Submit the billing form.
4. Check the calculated total.
5. Verify that the billing record is stored.

---

## Triage

1. Enter a severity score from `1` to `10`.
2. Submit the form.
3. Check the assigned room.
4. Verify that the triage record is stored.

---

# 🤖 AI-Assisted Development

AI tools were used as a **learning and development assistant** during the project.

AI assistance included:

### 💡 Understanding

* Flask concepts
* Docker concepts
* ngrok concepts
* Git and GitHub
* Python programming
* SQLite
* Web development concepts

### 💻 Development

* Python / Flask development
* HTML
* CSS
* JavaScript
* SQLite database logic
* Input validation
* Appointment date validation
* UI improvements

### 🐛 Troubleshooting

AI was used to help understand and troubleshoot:

* Flask errors
* Docker errors
* Git problems
* ngrok installation issues
* Website update issues
* Date validation problems
* Environment configuration

### 📝 Documentation

AI assistance was also used for:

* README documentation
* Pseudocode
* IPO tables
* Flowcharts
* Presentation preparation
* Technical explanations

> **Important:** AI was used as a learning and development assistant. The project was tested and implemented by the student.

---

# 🧠 Example AI Prompts

Some examples of prompts used during development include:

### Docker

```text
What is Docker and how do I use it for my Flask CareBridge Hospital application?
```

### ngrok

```text
What is ngrok and how can I use it to expose my Flask application running on port 5000?
```

### Debugging

```text
My Docker container is running but my website is not updating. Help me troubleshoot it.
```

### Git

```text
I have conflicts during git pull --rebase. How do I resolve them without losing my changes?
```

### Appointment Date Validation

```text
Make the appointment date validation require a date at least 8 days from today.
```

---

# 🔐 Security & Data Considerations

CareBridge Hospital is an **educational and demonstration project**.

Please observe the following:

* Do not enter real patient information.
* Do not enter sensitive medical information.
* The SQLite database is intended for development and demonstration.
* The temporary ngrok URL may change when the tunnel is restarted.
* Do not share sensitive information through the public ngrok URL.
* Port `5000` must be available.
* Docker Desktop must be running before using Docker commands.

---

# ⚠️ Troubleshooting

## Docker command not recognised

Make sure:

1. Docker Desktop is installed.
2. Docker Desktop is running.
3. Docker's environment is available in PowerShell.

Check:

```powershell
docker --version
```

Then:

```powershell
docker info
```

---

## Container is not running

Check:

```powershell
docker compose ps
```

Then view logs:

```powershell
docker compose logs
```

You can rebuild the application:

```powershell
docker compose up --build
```

---

## Website is not updating

Try rebuilding the Docker image:

```powershell
docker compose down
docker compose up --build -d
```

Then refresh:

```text
http://localhost:5000
```

If necessary, check the logs:

```powershell
docker compose logs
```

---

## ngrok command not recognised

Because ngrok was installed through the Microsoft Store, PowerShell may not recognise:

```powershell
ngrok
```

Instead, locate the executable:

```powershell
$pkg = Get-AppxPackage ngrok.ngrok

$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
```

Then run:

```powershell
& "$ngrokExe" http 5000
```

---

## ngrok cannot connect to CareBridge

First confirm that CareBridge works locally:

```text
http://localhost:5000
```

Then confirm Docker is running:

```powershell
docker compose ps
```

Then start ngrok:

```powershell
& "$ngrokExe" http 5000
```

---

# 📦 Requirements

## Local Development

* Python 3.x
* Flask
* SQLite
* Git

## Containerised Development

* Docker Desktop
* Docker Compose

## Public Demonstration

* ngrok

---

# 🚀 Quick Start

For the fastest setup using Docker Compose:

### Step 1 — Open the project

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"
```

### Step 2 — Start CareBridge

```powershell
docker compose up --build -d
```

### Step 3 — Check the container

```powershell
docker compose ps
```

### Step 4 — Open locally

```text
http://localhost:5000
```

### Step 5 — Locate ngrok

```powershell
$pkg = Get-AppxPackage ngrok.ngrok

$ngrokExe = (Get-ChildItem $pkg.InstallLocation -Recurse -Filter "ngrok.exe" -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
```

### Step 6 — Start ngrok

```powershell
& "$ngrokExe" http 5000
```

### Step 7 — Open the public URL

Copy the HTTPS URL displayed under:

```text
Forwarding
```

Example:

```text
https://xxxx.ngrok-free.dev
```

---

# 📊 Technology Architecture

```text
┌─────────────────────────────────────────┐
│               User / Staff              │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│              Web Browser                │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│                 ngrok                   │
│          Public HTTPS Tunnel            │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│           Docker Container              │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │          Flask Application        │  │
│  │              app.py               │  │
│  └──────────────────┬────────────────┘  │
│                     │                   │
│                     ▼                   │
│  ┌───────────────────────────────────┐  │
│  │          SQLite Database          │  │
│  │          carebridge.db            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

# 📌 Project Information

| Item                     | Details                             |
| ------------------------ | ----------------------------------- |
| **Project**              | CareBridge Hospital                 |
| **Application**          | Hospital Management Web Application |
| **Programming Language** | Python                              |
| **Framework**            | Flask                               |
| **Database**             | SQLite                              |
| **Frontend**             | HTML / CSS / JavaScript             |
| **Containerisation**     | Docker                              |
| **Container Management** | Docker Compose                      |
| **Public Tunnel**        | ngrok                               |
| **Version Control**      | Git                                 |
| **Repository Hosting**   | GitHub                              |
| **Application Port**     | 5000                                |

---

# 🔗 GitHub Repository

**CareBridge Hospital**

Repository:

`https://github.com/jiye130309-arch/CareBridge-Hospital`

---

# 🎯 Project Workflow

```text
                DEVELOPMENT
                     │
                     ▼
                Write Code
                     │
                     ▼
               Test Locally
                     │
                     ▼
               Git / GitHub
                     │
                     ▼
              Docker Build
                     │
                     ▼
             Docker Container
                     │
                     ▼
              localhost:5000
                     │
                     ▼
                  ngrok
                     │
                     ▼
             Public HTTPS URL
                     │
                     ▼
              Demonstration
```

---

# 🏁 Conclusion

CareBridge Hospital demonstrates how traditional hospital management workflows can be transformed into a modern web-based application.

The project combines:

* **Flask** for the web application
* **SQLite** for data storage
* **HTML/CSS** for the user interface
* **Docker** for environment standardisation
* **Docker Compose** for container management
* **Git/GitHub** for version control
* **ngrok** for public access
* **AI tools** for learning, development and troubleshooting

The project provides a practical example of developing, containerising, testing and demonstrating a web-based application.

---

## ⚠️ Educational Use

**CareBridge Hospital is intended for educational and demonstration purposes only.**

Do not use this application to store or process real patient data or sensitive medical information.

---

**🏥 CareBridge Hospital — Modernising Hospital Management Through Web Technology.**
