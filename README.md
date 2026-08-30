# 🏎️ Car Clash 3D — Cloud-Connected WebGL Game

An interactive, full-stack 3D WebGL car racing game integrated with a Python Flask REST API and PostgreSQL database, hosted on AWS EC2 with Nginx reverse proxy and SSL encryption.

🌐 **Live Demo:** [https://carclash.duckdns.org](https://carclash.duckdns.org)

---

## 🚀 Key Features

* **3D Racing Engine:** Built in Unity and compiled to optimized WebGL for in-browser gameplay.
* **User Management & Auth:** Secure player authentication, session tracking, and user profiles powered by Flask.
* **Persistent Database:** PostgreSQL integration for tracking race records, player scores, and vehicle stats.
* **Cloud Infrastructure:** Hosted on **AWS EC2 (Ubuntu)** with automated WSGI process management using **Gunicorn**.
* **Reverse Proxy & Security:** Production-grade **Nginx** configuration with custom DNS routing and automated **SSL/TLS (Certbot / Let's Encrypt)**.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Game Engine** | Unity (C#, WebGL Build) |
| **Backend** | Python, Flask, Gunicorn |
| **Database** | PostgreSQL, SQLite3 (Local Dev) |
| **Frontend UI** | HTML5, CSS3, Modern JavaScript |
| **Cloud & DevOps** | AWS EC2, Nginx, Certbot (SSL), Git/GitHub |

---

## ⚙️ Architecture Overview
