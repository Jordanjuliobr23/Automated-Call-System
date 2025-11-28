# 📲🔳🏷️Automated Call System 

## 📋 About the project:
- This is a academy project from discipline **Integrative Project**
- The project consists of developing a solution for classroom attendance automation.
- Authentication occurs through an application that generates QR codes, which redirects to the IFRN institutional login page (SUAP).
- After the student has been redirected to the SUAP portal, they will authenticate with their enrollment number and institutional password. This will allow the system to confirm their attendance in the current class.


---

## ⚙︎ Manager from the project:


## 🛠️ Project Structure

This project is divided into multiple services:

- **Frontend (Django)** — responsável: Ian Guilherme 
- **Banco de Dados** — responsável: Tamires Angélica
- **Docker Compose** — responsável: Jordan Julio 
- **Nginx Proxy** — responsável: Pedro Jordan

---

## 🚀 How to Run the Proxy (Nginx)

The Nginx proxy routes requests to the frontend and backend services and serves static files.

### Prerequisites
- Docker and Docker Compose installed
- Services `frontend` and `backend` must be running on the same Docker network (`qr_network`)


