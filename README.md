# 🏎️ Car Clash 3D — Cloud-Connected WebGL Game & Infrastructure

An enterprise-grade, cloud-deployed 3D WebGL car racing application seamlessly integrated with a Python Flask REST backend, PostgreSQL persistent storage, and AWS infrastructure fronted by Nginx with automated SSL/TLS encryption.

* **Live Demo:** https://carclash.duckdns.org
* **GitHub Repository:** https://github.com/sayyedmusaib91-code/Car-Game-project.git

---

## 🌟 Overview

Car Clash 3D demonstrates end-to-end cloud engineering and full-stack software development by bridging a high-performance Unity WebGL game engine with an enterprise-ready Linux web server architecture. 

The project delivers a lag-free, browser-native 3D gaming experience while securely handling player authentication, session persistence, and dynamic user profiles via a hardened cloud production pipeline.

---

## 🚀 Key Features

* **Browser-Native 3D Engine:** Built in Unity using custom C# physics, asset compression, and memory-optimized WebGL compilation for cross-browser gameplay without external plugins.
* **Authentication & User Sessions:** Secure registration, encrypted login, role-based driver identities, and persistent sessions managed by a Python Flask REST API.
* **Production Cloud Deployment:** Hosted on AWS EC2 (Ubuntu Linux) with multi-worker Gunicorn WSGI process orchestration for concurrent user loads.
* **Hardened Security & Network Layer:** Production Nginx reverse proxy implementing HTTP-to-HTTPS automatic redirection, custom AWS Security Groups, and automated TLS lifecycle management via Certbot / Let's Encrypt.
* **Persistent Relational Database:** Structured PostgreSQL relational schema managing driver profiles, vehicle inventory, race metadata, and dynamic stats.
* **Custom Web HUD:** Responsive, cyber-themed UI built with HTML5, CSS3, and JavaScript, featuring car inspection HUDs, custom track selection, and audio telemetry.

---

## 🛠️ Technology Stack

* **Game Engine & Client:** Unity 3D, C#, WebGL Canvas Runtime
* **Backend Framework:** Python 3, Flask, Gunicorn WSGI Server, Werkzeug Security
* **Database & Persistence:** PostgreSQL, psycopg2, SQLite3
* **Frontend Interface:** HTML5, CSS3, ES6+ JavaScript, FontAwesome, Google Web Fonts
* **Cloud & Infrastructure:** Amazon Web Services (AWS EC2, VPC, Security Groups, IAM)
* **Web Server & Networking:** Nginx Reverse Proxy, Let's Encrypt SSL/TLS, DNS Mapping, SSH
* **DevOps & Workflow:** Git, GitHub, Linux Bash CLI, SFTP Automation

---

## ⚙️ Cloud System Architecture Flow

1. **Client Browser / Player Layer:** The player interacts with the responsive Web HUD and the Unity WebGL Canvas in any modern web browser.
2. **Secure Transport Layer:** Incoming requests route through HTTPS (Port 443) to the AWS EC2 instance.
3. **Nginx Web Server & Reverse Proxy:** Nginx terminates SSL/TLS, enforces HTTP to HTTPS redirection, and securely proxies requests internally to `127.0.0.1:5000`.
4. **Gunicorn WSGI Process Manager:** Manages multi-threaded worker processes to handle concurrent REST API requests smoothly.
5. **Flask Backend Application:** Authenticates users, validates session cookies, manages game routes, and executes business logic.
6. **PostgreSQL Relational Database:** Stores user credentials, game telemetry, race statistics, and profile data persistently.

---

## 📁 Repository Structure

* `app.py` — Flask Application Controller & REST API Endpoints
* `database.py` — PostgreSQL Database Connection & Query Logic
* `requirements.txt` — Python Dependencies & Environment Packages
* `static/BugattiBuild/` — Unity WebGL Build Artifacts (Data, Framework, Wasm)
* `static/css/` — Custom Stylesheets & HUD Themes
* `static/image/` — High-Resolution Game Assets, Banners & Vehicle Renders
* `static/sounds/` — Engine SFX, Audio UI Effects & Background Music
* `templates/` — Jinja2 HTML Templates (Garage HUD, Login, Signup, Profile, Store)

---

## 🛡️ Production Specifications

* **Operating System:** Ubuntu Server LTS
* **Process Manager:** Gunicorn WSGI with 3 worker processes
* **Web Server:** Nginx Reverse Proxy (Port 80 to 443 redirect)
* **SSL/TLS:** Auto-renewing certificates via Let's Encrypt Certbot
* **Static Assets:** Optimized for handling high-volume WebGL binary payloads

---

## 👨‍💻 Author

**Musaib Sayyed**  
Cloud & DevOps Enthusiast | Computer Science Student  
* **Portfolio:** https://musaib-portfolio.duckdns.org  
* **GitHub:** https://github.com/sayyedmusaib91-code
*
