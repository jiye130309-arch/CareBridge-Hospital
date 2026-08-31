# 🏥 CareBridge Hospital

A web-based hospital management system developed using **Python Flask, SQLite, HTML, CSS, Docker, Docker Compose, Git, GitHub, and ngrok**.

CareBridge Hospital modernises traditional hospital management workflows into a web-based application that allows hospital staff to manage **patients, appointments, billing, and triage** through a simple interface.

> **Project Type:** Educational / Web Migration Project
> **Application:** Hospital Management Web Application
> **Framework:** Flask
> **Database:** SQLite
> **Containerisation:** Docker
> **Container Management:** Docker Compose
> **Public Access:** ngrok

---

# 📌 Project Overview

CareBridge Hospital is a Flask-based hospital management web application developed as part of a web migration project.

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
* 🌐 ngrok public HTTPS tunnelling
* 🔐 Input validation
* 💾 Persistent database storage

---

# 🛠️ Technologies Used

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| Python         | Main programming language              |
| Flask          | Web application framework              |
| SQLite         | Database management                    |
| HTML           | Web page structure                     |
| CSS            | User interface styling                 |
| JavaScript     | Client-side functionality              |
| Docker         | Application containerisation           |
| Docker Compose | Container configuration and management |
| ngrok          | Public HTTPS tunnel                    |
| Git            | Version control                        |
| GitHub         | Source code repository                 |

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

* GP
* Specialist

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

* Subsidised
* Private

The calculated bill is saved into the SQLite database.

---

## 4. 🚑 Triage Room Assignment

Staff can enter a patient's severity score from **1 to 10**.

The system automatically assigns an appropriate room based on the severity level.

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

The project also includes:

```text
carebridge.sql
```

for SQL/database definitions.

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

Docker is used as an environment standardiser for the CareBridge Hospital application.

The Docker image is based on:

```text
python:3.12-alpine
```

The application runs inside a Docker container on port:

```text
5000
```

### Why Docker?

Docker provides:

* Consistent development environment
* Dependency management
* Application isolation
* Reproducible setup
* Easier deployment
* Easier project demonstration

---

# 🐳 Dockerfile

The Dockerfile is responsible for creating the CareBridge Hospital container environment.

Example structure:

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

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

# 📦 Docker Compose

Docker Compose is the recommended way to run CareBridge Hospital.

The configuration file is:

```text
docker-compose.yml
```

## Docker Compose Configuration

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

### Configuration Explanation

| Configuration             | Purpose                                        |
| ------------------------- | ---------------------------------------------- |
| `services`                | Defines the application service                |
| `carebridge`              | Name of the CareBridge service                 |
| `build: .`                | Builds the image using the Dockerfile          |
| `container_name`          | Gives the container a fixed name               |
| `ports`                   | Maps host port `5000` to container port `5000` |
| `volumes`                 | Persists the SQLite database                   |
| `restart: unless-stopped` | Restarts the container unless manually stopped |

---

# 🚀 Running with Docker Compose

## 1. Open the Project Directory

Open PowerShell:

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"
```

If the repository is stored somewhere else, use that directory instead.

---

## 2. Build and Start the Application

```powershell
docker compose up --build
```

The application will be available at:

```text
http://localhost:5000
```

---

## 3. Run in the Background

For normal demonstrations:

```powershell
docker compose up --build -d
```

---

## 4. Check the Container

```powershell
docker compose ps
```

You should see the CareBridge container running with port `5000` mapped.

---

## 5. View Application Logs

```powershell
docker compose logs
```

To continuously follow the logs:

```powershell
docker compose logs -f
```

---

## 6. Stop the Application

```powershell
docker compose down
```

---

# 💾 SQLite Database Persistence

The project uses a Docker volume mapping for the SQLite database:

```yaml
volumes:
  - ./carebridge.db:/app/carebridge.db
```

This maps the SQLite database on the host machine to the database location inside the Docker container.

This allows the database to remain available when the Docker container is restarted or recreated.

---

# 🌐 ngrok

ngrok is used to make the locally running CareBridge Hospital application accessible through a public HTTPS URL.

The CareBridge application runs on:

```text
http://localhost:5000
```

The architecture is:

```text
Internet
   │
   ▼
ngrok Public HTTPS URL
   │
   ▼
localhost:5000
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
docker compose up --build -d
```

Check the container:

```powershell
docker compose ps
```

Test the local application:

```text
http://localhost:5000
```

Make sure CareBridge Hospital works locally before starting ngrok.

---

## 2. Check ngrok

ngrok is installed and configured on the Windows system.

Check the installed version:

```powershell
ngrok version
```

Expected output:

```text
ngrok version 3.x.x
```

---

## 3. Configure the ngrok Authentication Token

Configure your own ngrok authentication token:

```powershell
ngrok config add-authtoken "YOUR_NGROK_AUTHTOKEN"
```

Replace:

```text
YOUR_NGROK_AUTHTOKEN
```

with your own token.

### ⚠️ Important

**Never put your actual ngrok authentication token in this README or commit it to GitHub.**

Keep the token private.

Check the configuration:

```powershell
ngrok config check
```

---

# 🚀 Start the ngrok Tunnel

Once CareBridge Hospital is running on port `5000`, open another PowerShell window.

Run:

```powershell
ngrok http 5000
```

ngrok will create a public HTTPS forwarding URL.

Example:

```text
Forwarding
https://xxxx-xxxx.ngrok-free.app -> http://localhost:5000
```

Copy the HTTPS URL and open it in a browser.

The public URL can also be accessed from another device.

---

# ⚡ Quick ngrok Command

Because ngrok is available through the Windows PATH, the tunnel can be started directly with:

```powershell
ngrok http 5000
```

No additional executable path configuration is required.

---

# 🔄 Complete Startup Sequence

The normal CareBridge Hospital demonstration workflow is:

### Terminal 1 — Docker

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"

docker compose up --build -d

docker compose ps
```

Test:

```text
http://localhost:5000
```

### Terminal 2 — ngrok

```powershell
ngrok http 5000
```

Then copy the HTTPS URL displayed under:

```text
Forwarding
```

Example:

```text
https://xxxx-xxxx.ngrok-free.app
```

---

# 🔄 Complete System Workflow

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
                    │ localhost:5000  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Docker Compose  │
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

## Check Project Status

```powershell
git status
```

## Add Changes

```powershell
git add .
```

## Commit Changes

```powershell
git commit -m "Update CareBridge Hospital"
```

## Pull Changes

```powershell
git pull --rebase origin main
```

## Push Changes to GitHub

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
git pull --rebase origin main
   ↓
git push origin main
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
4. Make sure the appointment is at least 8 days from today.
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

# ⚠️ Troubleshooting

## Flask Is Not Installed

If you run:

```powershell
python app.py
```

and receive:

```text
ModuleNotFoundError: No module named 'flask'
```

you can install Flask locally:

```powershell
python -m pip install flask
```

For the normal CareBridge setup, Docker Compose is recommended because the required Python dependencies are installed inside the Docker container.

---

## Docker Command Not Recognised

Check:

```powershell
docker --version
```

Then:

```powershell
docker info
```

Make sure Docker Desktop is installed and running.

---

## Container Is Not Running

Check:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs
```

Rebuild the application:

```powershell
docker compose down
docker compose up --build -d
```

---

## Website Is Not Updating

If application changes are not appearing, rebuild the Docker image:

```powershell
docker compose down
docker compose up --build -d
```

Then refresh:

```text
http://localhost:5000
```

You can also check:

```powershell
docker compose logs -f
```

---

## ngrok Command Not Recognised

If PowerShell displays:

```text
ngrok : The term 'ngrok' is not recognized
```

make sure you have:

1. Installed ngrok.
2. Added ngrok to the Windows PATH.
3. Closed and reopened PowerShell.

Then test:

```powershell
ngrok version
```

If the version appears, start the tunnel:

```powershell
ngrok http 5000
```

---

## ngrok Cannot Connect to CareBridge

First check that CareBridge works locally:

```text
http://localhost:5000
```

Then check Docker:

```powershell
docker compose ps
```

If the container is not running:

```powershell
docker compose up --build -d
```

Then start:

```powershell
ngrok http 5000
```

---

## Port 5000 Is Already in Use

Check which process is using port `5000`:

```powershell
netstat -ano | findstr :5000
```

If Docker is already running CareBridge on port `5000`, do not start another Flask instance using:

```powershell
python app.py
```

Use the Docker container instead.

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
* ngrok authentication token

---

# 🚀 Quick Start

For the fastest CareBridge Hospital demonstration:

### Step 1 — Open the Project

```powershell
cd "C:\Users\jiye1\Downloads\CareBridge-Hospital"
```

### Step 2 — Start Docker

```powershell
docker compose up --build -d
```

### Step 3 — Check Docker

```powershell
docker compose ps
```

### Step 4 — Test Locally

Open:

```text
http://localhost:5000
```

### Step 5 — Start ngrok

Open another PowerShell window:

```powershell
ngrok http 5000
```

### Step 6 — Open the Public URL

Copy the HTTPS URL shown by ngrok:

```text
https://xxxx-xxxx.ngrok-free.app
```

---

# 🤖 AI-Assisted Development

AI tools were used as learning and development assistants throughout the project.

AI assistance included:

### 💡 Understanding

* Flask concepts
* Docker concepts
* Docker Compose
* ngrok
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

### Docker

```text
What is Docker and how do I use it for my Flask CareBridge Hospital application?
```

### Docker Compose

```text
How can I use Docker Compose to run my Flask CareBridge Hospital application on port 5000?
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
* Never share your ngrok authentication token.
* Never commit the ngrok authentication token to GitHub.
* The temporary ngrok URL may change when the tunnel is restarted.
* Do not share sensitive information through the public ngrok URL.
* Docker Desktop must be running before using Docker commands.
* Port `5000` must be available.

---

# 🌐 Public Access with ngrok

The standard ngrok command creates a temporary public HTTPS URL:

```powershell
ngrok http 5000
```

The generated URL may change when the ngrok tunnel is stopped and started again.

For a fixed public address, a reserved ngrok domain or custom domain can be configured separately through the ngrok account.

---

# 📊 Technology Architecture

| Layer                | Technology            |
| -------------------- | --------------------- |
| Frontend             | HTML, CSS, JavaScript |
| Backend              | Python, Flask         |
| Database             | SQLite                |
| Containerisation     | Docker                |
| Container Management | Docker Compose        |
| Public Tunnel        | ngrok                 |
| Version Control      | Git                   |
| Repository           | GitHub                |

---

# 📌 Project Information

| Item                 | Details                             |
| -------------------- | ----------------------------------- |
| Project              | CareBridge Hospital                 |
| Application          | Hospital Management Web Application |
| Programming Language | Python                              |
| Framework            | Flask                               |
| Database             | SQLite                              |
| Frontend             | HTML / CSS / JavaScript             |
| Containerisation     | Docker                              |
| Container Management | Docker Compose                      |
| Public Tunnel        | ngrok                               |
| Version Control      | Git                                 |
| Repository Hosting   | GitHub                              |
| Application Port     | 5000                                |

---

# 🔗 GitHub Repository

**CareBridge Hospital**

```text
https://github.com/jiye130309-arch/CareBridge-Hospital
```

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
               Docker Compose
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

* 🐍 **Flask** for the web application
* 🗄️ **SQLite** for data storage
* 🎨 **HTML/CSS/JavaScript** for the user interface
* 🐳 **Docker** for containerisation
* 📦 **Docker Compose** for container management
* 🔧 **Git/GitHub** for version control
* 🌐 **ngrok** for public HTTPS access
* 🤖 **AI tools** for learning, development and troubleshooting

The project provides a practical example of developing, testing, containerising, version-controlling and demonstrating a web-based hospital management system.

---

# ⚠️ Educational Use

CareBridge Hospital is intended for **educational and demonstration purposes only**.

Do not use this application to store or process real patient data or sensitive medical information.

---

# 🏥 CareBridge Hospital

**Modernising Hospital Management Through Web Technology**
