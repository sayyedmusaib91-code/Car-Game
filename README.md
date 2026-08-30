# 🏎️ Car Clash 3D — Cloud-Connected WebGL Game & Infrastructure

> An enterprise-grade, cloud-deployed 3D WebGL car racing application seamlessly integrated with a Python Flask REST backend, PostgreSQL persistent storage, and AWS infrastructure fronted by Nginx with automated SSL/TLS encryption.

🌐 **Live Demo:** [https://carclash.duckdns.org](https://carclash.duckdns.org)  
📦 **Source Code:** [github.com/sayyedmusaib91-code/Car-Game-project](https://github.com/sayyedmusaib91-code/Car-Game-project)

---

## 🌟 Executive Summary

**Car Clash 3D** demonstrates end-to-end cloud engineering and full-stack software development by bridging a high-performance Unity WebGL game engine with an enterprise-ready Linux web server architecture. 

The project delivers a lag-free, browser-native 3D gaming experience while securely handling player authentication, real-time telemetry, session persistence, and dynamic user leaderboards via a hardened cloud production pipeline.

---

## 🚀 Key Features & Highlights

* **Browser-Native 3D Racing Engine:** Built in Unity using custom C# physics, asset compression, and memory-optimized WebGL compilation for cross-browser gameplay without plugins.
* **Robust Authentication & User Sessions:** Secure signup, encrypted login, role-based driver identities, and persistent sessions managed by a Python Flask REST API.
* **Production-Grade Cloud Deployment:** Hosted on **AWS EC2 (Ubuntu Linux)** with multi-worker **Gunicorn WSGI** process orchestration for concurrent user loads.
* **Hardened Security & Network Layer:** Production **Nginx** reverse proxy implementing HTTP-to-HTTPS automatic redirection, custom AWS Inbound/Outbound Security Groups, and automated TLS lifecycle management via **Certbot (Let's Encrypt)**.
* **Persistent Relational Database:** Structured **PostgreSQL** relational schema managing driver profiles, vehicle inventory, race metadata, and dynamic stats.
* **Sleek Custom Web HUD:** Responsive, modern cyber-themed UI built with HTML5, CSS3, and JavaScript, featuring car inspection HUDs, custom track selection, and audio telemetry.

---

## 🛠️ Comprehensive Tech Stack

* **Game Engine & Client:** Unity 3D, C#, WebGL Canvas Runtime
* **Backend Services:** Python 3, Flask, Gunicorn WSGI Server, Werkzeug Security
* **Database & Persistence:** PostgreSQL, psycopg2, SQLite3 (Local Development)
* **Frontend Web HUD:** HTML5, CSS3, ES6+ JavaScript, FontAwesome, Google Web Fonts
* **Cloud & Infrastructure:** Amazon Web Services (AWS EC2, VPC, Security Groups, IAM)
* **Networking & Web Servers:** Nginx Reverse Proxy, Let's Encrypt SSL/TLS, DNS Configuration, SSH
* **DevOps & Tooling:** Git, GitHub, Linux Bash CLI, SFTP Automation

---

## ⚙️ Cloud System Architecture

```text
               +-------------------------------------------------------------+
               |                   Client Browser / Player                   |
               |          (HTML5 / CSS3 / JavaScript / Unity WebGL)          |
               +------------------------------+------------------------------+
                                              |
                                              | HTTPS (Port 443) / WSS
                                              v
               +-------------------------------------------------------------+
               |                   AWS EC2 Cloud Instance                    |
               |                                                             |
               |   +-----------------------------------------------------+   |
               |   |            Nginx Hardened Web Server                |   |
               |   |  - Reverse Proxy Layer                              |   |
               |   |  - SSL/TLS Termination (Let's Encrypt Certbot)     |   |
               |   |  - Port 80 -> Port 443 Auto-Redirect                |   |
               |   +--------------------------+--------------------------+   |
               |                              |                              |
               |                              | Reverse Proxy (127.0.0.1)    |
               |                              v                              |
               |   +-----------------------------------------------------+   |
               |   |            Gunicorn Multi-Worker WSGI               |   |
               |   |             (Process & Concurrency Manager)         |   |
               |   +--------------------------+--------------------------+   |
               |                              |                              |
               |                              v                              |
               |   +-----------------------------------------------------+   |
               |   |                  Flask REST API                     |   |
               |   |     (Auth, Telemetry, Sessions & Endpoints)         |   |
               |   +--------------------------+--------------------------+   |
               |                              |                              |
               |                              | Relational Queries / SQL     |
               |                              v                              |
               |   +-----------------------------------------------------+   |
               |   |             PostgreSQL Database Service             |   |
               |   |     (Users, Game Stats, Profiles, Leaderboards)     |   |
               |   +-----------------------------------------------------+   |
               +-------------------------------------------------------------+
