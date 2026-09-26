# 🛡️ SentinelAI: Adaptive Malicious Insider Threat Detection

An end-to-end **cybersecurity research framework and data pipeline** designed to detect and respond to **adaptive insider threats** using a **Bayesian Stackelberg Game**.

Unlike traditional anomaly detection systems that rely on fixed behavioral patterns, SentinelAI models how attackers can change their behavior to avoid detection. It combines **Game Theory, Explainable AI (XAI), and Post-Quantum Cryptography (PQC)** to create an adaptive and secure threat detection environment.

<!-- 📸 HERO SCREENSHOT PLACEHOLDER -->
![SentinelAI Main Dashboard](./screenshots/hero-dashboard.png)

*(Replace this with a wide screenshot of the main Executive SOC Dashboard showing the SHAP chart and key metrics.)*

## 🧰 Tech Stack

🐍 **Python 3.10** &nbsp;&nbsp; ⚡ **FastAPI** &nbsp;&nbsp; ⚛️ **React 18** &nbsp;&nbsp; 🐘 **PostgreSQL**  
🤖 **Scikit-Learn** &nbsp;&nbsp; 🎨 **Tailwind CSS** &nbsp;&nbsp; 📊 **Recharts**  
🎮 **RASRO / Stackelberg Game Theory** &nbsp;&nbsp; 🔐 **Post-Quantum Cryptography**  
🔑 **ML-KEM** &nbsp;&nbsp; ✍️ **ML-DSA** &nbsp;&nbsp; 🔎 **SHAP**

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-20232A?style=flat&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-22B5BF?style=flat&logo=react&logoColor=white)
![PQC](https://img.shields.io/badge/Post--Quantum_Cryptography-512BD4?style=flat)
![ML--KEM](https://img.shields.io/badge/ML--KEM-Key_Encapsulation-6A1B9A?style=flat)
![ML--DSA](https://img.shields.io/badge/ML--DSA-Digital_Signatures-8E24AA?style=flat)

---

## 📌 Problem Statement

Traditional insider threat detection systems often depend on fixed behavioral patterns. However, attackers can **adapt their behavior when they realize they are being monitored**.

For example, when a system detects a large data exfiltration attempt, an attacker may switch to a slower and less noticeable approach.

SentinelAI addresses this problem by modeling the interaction between the **defender and the attacker as a dynamic game**. This allows the system to track changes in attacker behavior and evaluate how well the defense responds.

The system uses **RASRO (Risk-Adaptive Security Response Optimization)** to evaluate the changing attacker state and determine an appropriate defensive response based on historical interactions and calculated game-theoretic metrics.

> **A dynamic Stackelberg Game Engine combined with Explainable AI and post-quantum-secure audit logging for adaptive insider threat detection.**

---

## 🔥 Key Features

### 1. 🎮 Dynamic Stackelberg Game Engine — RASRO

SentinelAI uses a **Risk-Adaptive Security Response Optimization (RASRO)** approach to model the interaction between an adaptive insider and the SOC.

- **Multi-Turn Interactions:** Models cybersecurity as a dynamic game where the SOC (Leader) and Insider (Follower) respond to each other's actions over multiple turns.
- **Adaptive Response:** The defense response changes based on the current threat state and previous attacker behavior.
- **Stateful Evaluation:** Uses historical interaction data stored in PostgreSQL instead of treating every event as an isolated incident.
- **Attacker Adaptation Score (AAS):** Measures how much the attacker's strategy changes between interactions.
- **Response Effectiveness Score (RES):** Measures how effectively the previous defensive action handled the current threat.
- **Mitigation Decisions:** Uses the evaluated state to support actions such as `REVOKE_SESSION`, `RESTRICT_ACCESS`, and other security responses.

### 2. 🤖 Explainable AI (XAI) Pipeline

SentinelAI combines machine learning with explainability to identify unusual user behavior and understand why an event was flagged.

- **Multivariate Anomaly Detection:** Uses **Isolation Forest** and **One-Class SVM** to analyze behavioral signals such as data transferred, login hours, and sensitive file access.
- **Tree SHAP Attribution:** Shows which behavioral features contributed most to the anomaly score.
- **Analyst-Friendly Results:** Provides interpretable feature contributions instead of only returning a binary anomaly decision.

### 3. 🔐 Post-Quantum Cryptography (PQC)

SentinelAI includes a post-quantum cryptography layer to protect sensitive security decisions and audit records.

#### 🔑 ML-KEM — Key Encapsulation

**ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism)** is used for post-quantum secure key establishment.

It provides a way for the system to establish shared cryptographic keys while being designed to remain secure against attacks from future quantum computers.

#### ✍️ ML-DSA — Digital Signatures

**ML-DSA (Module-Lattice-Based Digital Signature Algorithm)** is used to digitally sign important security decisions and audit records.

The system can cryptographically sign:

- Telemetry evaluation results
- Orchestrator decisions
- Incident records
- Mitigation actions
- Audit events

This helps provide **integrity, authenticity, and tamper detection** for security records.

#### 🛡️ PQC-Protected Audit Trail

The combination of **ML-KEM and ML-DSA** provides the cryptographic layer used to protect sensitive communication and security records.

> **ML-KEM → Secure Key Establishment → ML-DSA → Signed Security Decisions → PostgreSQL Audit Record**

### 4. 📈 Interactive Ablation Simulator

- **Live React Dashboard:** Provides an interactive dashboard using Recharts to visualize telemetry and multi-cycle attack simulations.
- **Scenario-Based Simulation:** Supports scenarios such as **Massive Exfiltration** and **Stealth Evasion**.
- **Research Validation:** Compares static detection approaches with the adaptive game-theoretic approach through live graphs and metrics.
- **Multi-Cycle Evaluation:** Allows attacker behavior and defensive responses to be observed across multiple interaction turns.

---

## 📊 Platform Screenshots

### 🔑 Secure Access Portal

> Role-based login system that protects access to the SOC dashboard and backend resources.

<!-- 📸 LOGIN SCREENSHOT -->
![Secure Login](./screenshots/login-page.png)

### 🖥️ Executive SOC Dashboard

> Displays incoming telemetry, active security incidents, anomaly scores, and Tree SHAP feature attribution.

<!-- 📸 SOC DASHBOARD SCREENSHOT -->
![Executive SOC Dashboard](./screenshots/soc-dashboard.png)

### 🔐 Cryptographic Audit Ledger

> Displays the historical record of telemetry events, anomaly decisions, and Stackelberg mitigation actions.

<!-- 📸 AUDIT SCREENSHOT -->
![Audit Telemetry](./screenshots/audit-telemetry.png)

### 🎯 Adaptive Attacker Simulator

> Allows users to run multi-cycle attack simulations using custom telemetry or predefined scenarios such as **Massive Exfiltration** and **Stealth Evasion**.

<!-- 📸 SIMULATOR SCREENSHOT -->
![Threat Simulator Input](./screenshots/threat-simulator.png)

### 📈 Research Ablation Study & Time-Series Graphs

> Displays how the **Attacker Adaptation Score (AAS)** and **Response Effectiveness (RES)** change across multiple attack turns.

<!-- 📸 GRAPHS SCREENSHOT -->
![Ablation Study Graphs](./screenshots/ablation-graphs.png)

### 🔑 ML-KEM & ML-DSA Post-Quantum Cryptography

> Terminal demonstration showing the ML-KEM key encapsulation process and ML-DSA digital signature generation and verification.

<!-- 📸 PQC TERMINAL SCREENSHOT -->
![ML-KEM and ML-DSA Terminal](./screenshots/pqc-terminal.png)

### 🔄 End-to-End Decision & Enforcement Workflow

> End-to-end flow showing how telemetry moves through anomaly detection, XAI analysis, RASRO evaluation, mitigation decision, cryptographic protection, and enforcement.

<!-- 📸 END-TO-END WORKFLOW FLOWCHART -->
![End-to-End Decision and Enforcement Workflow](./screenshots/end-to-end-workflow.png)

### 🏗️ System Architecture

> High-level architecture showing the interaction between the frontend, backend services, machine learning pipeline, RASRO engine, PostgreSQL database, and post-quantum cryptography layer.

<!-- 📸 ARCHITECTURE IMAGE -->
![SentinelAI System Architecture](./screenshots/architecture.png)

---

## 🏗️ Architecture & Data Modeling

### ⚙️ Backend & Data Pipeline

- **Core Framework:** FastAPI for REST API routing and backend services.
- **Database ORM:** SQLAlchemy for managing database models and application data.
- **Persistence:** PostgreSQL for structured data and historical state tracking.
- **Machine Learning:** Scikit-Learn using Isolation Forest, One-Class SVM, and SHAP for anomaly detection and explainability.
- **Game Engine:** RASRO-based Stackelberg evaluation for adaptive attacker-defender interactions.
- **Cryptography:** ML-KEM and ML-DSA for post-quantum key establishment and digital signatures.

### 💻 Frontend

- **Core:** React 18 with Axios for API communication.
- **Styling:** Tailwind CSS for the dark-mode SOC interface.
- **Visualization:** Recharts for interactive time-series graphs and data visualization.
- **Simulation:** Interactive threat telemetry and multi-cycle attack simulation interface.

### 🔐 Post-Quantum Security Layer

The PQC layer contains two main components:

**ML-KEM**
- Used for secure key encapsulation and key establishment.
- Provides post-quantum protection for cryptographic key exchange.

**ML-DSA**
- Used for digital signatures.
- Signs security decisions and audit records.
- Allows the system to verify that records have not been modified after signing.

---

## 🎮 Stackelberg Research Metrics

| Metric | Range | Description | Game Theory Role |
| :--- | :---: | :--- | :--- |
| **AAS** | `-1.0` to `1.0` | **Attacker Adaptation Score:** Measures how much the attacker's strategy changes. | Helps identify strategy changes such as **Aggressive → Stealth** behavior. |
| **RES** | `-1.0` to `1.0` | **Response Effectiveness:** Measures how well the SOC's previous action handled the current threat. | Helps determine whether actions such as **Revoke** or **Restrict** were effective. |

---

## 🔄 System Workflow

1. **📥 Telemetry Ingestion:** The React simulator sends behavioral telemetry to the FastAPI backend.
2. **🤖 XAI Inference:** The data is processed by the Isolation Forest and One-Class SVM models. Tree SHAP calculates the contribution of each feature.
3. **🎮 Stateful Game Evaluation:** The RASRO Stackelberg engine retrieves previous interaction data from PostgreSQL and evaluates the current attacker state.
4. **📊 AAS & RES Calculation:** The system calculates the **Attacker Adaptation Score (AAS)** and **Response Effectiveness (RES)** using the current and previous interaction states.
5. **🛡️ Mitigation Decision:** Based on the evaluated threat state, the orchestrator selects an appropriate security response such as `REVOKE_SESSION` or `RESTRICT_ACCESS`.
6. **🔑 PQC Key Protection:** ML-KEM is used as part of the post-quantum key establishment layer.
7. **✍️ Decision Signing:** The final mitigation decision and relevant audit information are digitally signed using **ML-DSA**.
8. **💾 Database Commit:** The signed record is stored in PostgreSQL as part of the audit trail.
9. **⚡ Enforcement & Visualization:** The selected security action is enforced and the frontend immediately updates the dashboard, metrics, and graphs.

---

## 🔐 PQC Security Flow

    Security Decision
           │
           ▼
       RASRO Engine
           │
           ▼
      Mitigation Action
           │
           ├──────────────► ML-KEM
           │                    │
           │                    ▼
           │             Secure Key Establishment
           │
           ▼
         ML-DSA
           │
           ▼
      Digital Signature
           │
           ▼
     Signed Audit Record
           │
           ▼
       PostgreSQL

---

## 🚀 Getting Started

### 📋 Prerequisites

- 🐍 Python 3.10+
- 🟢 Node.js v18+
- 🐘 PostgreSQL v15+

### 1. 🗄️ Database Setup

Create a local PostgreSQL database named:

`sentinelai_db`

Update the database URL in `backend/.env`:

`DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/sentinelai_db`

### 2. ⚡ Backend Installation

`cd backend`

`python -m venv venv`

**Windows:**

`venv\Scripts\activate`

**macOS/Linux:**

`source venv/bin/activate`

Install the dependencies:

`pip install -r requirements.txt`

Start the FastAPI server:

`uvicorn app.main:app --reload --port 8000`

The backend will start on:

`http://localhost:8000`

### 3. ⚛️ Frontend Installation

Open a new terminal and run:

`cd frontend`

`npm install`

Start the React dashboard:

`npm start`

The SOC Dashboard will be available at:

`http://localhost:3000`

From the dashboard, navigate to the **Threat Simulator** tab to run the attack simulations and ablation studies.

---

## 🧩 Project Structure

    SentinelAI/
    │
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   │   ├── pqc_kem.py
    │   │   │   └── pqc_dsa.py
    │   │   ├── models/
    │   │   └── services/
    │   ├── requirements.txt
    │   └── ...
    │
    ├── frontend/
    │   ├── src/
    │   ├── package.json
    │   └── ...
    │
    └── README.md

---

## 🔬 Research Focus

SentinelAI brings together several areas of cybersecurity and AI:

- 🎮 **Game Theory** — Modeling attacker-defender interactions through Stackelberg games and RASRO.
- 🤖 **Machine Learning** — Detecting unusual user behavior using Isolation Forest and One-Class SVM.
- 🔎 **Explainable AI** — Understanding why an event was flagged using Tree SHAP.
- 🎯 **Adaptive Threat Modeling** — Tracking how attackers change their behavior across multiple interactions.
- 🔐 **Post-Quantum Cryptography** — Using ML-KEM for key establishment and ML-DSA for digital signatures.
- 🛡️ **Security Enforcement** — Connecting threat evaluation to actions such as session revocation and access restriction.
- 📊 **Data Visualization** — Analyzing attacker adaptation and defensive response through interactive dashboards and time-series graphs.

The goal is to provide a practical research platform for studying **adaptive insider threats** by combining **Game Theory, Machine Learning, Explainable AI, and Post-Quantum Cryptography** in a single security workflow.
