# 🚀 LogMind AI: Transforming Raw Logs into Actionable Intelligence

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-High_Performance-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini API](https://img.shields.io/badge/Google_Gemini-LLM_Powered-orange.svg)](https://aistudio.google.com/)
[![Deployment](https://img.shields.io/badge/Deployed_on-Render-purple.svg)](https://render.com)

### 🚩 The Problem
Developers waste hours manually parsing through thousands of lines of logs during a production outage. This "log-diving" increases **MTTR (Mean Time To Recovery)** and delays critical bug fixes, leading to extended system downtime.

### ✅ The Solution
**LogMind AI** is a cloud-native diagnostic engine that transforms raw, chaotic system logs into high-fidelity incident reports. By integrating **Google's Gemini 1.5 Flash**, it doesn't just "search" for errors—it **reasons** through them to find the root cause and suggests the exact fix in seconds.

---

## 🌐 Live Production Access
The platform is fully deployed and operational on **Render**, providing a centralized hub for developers to diagnose system failures instantly without any local environment configuration.

👉 **Live Demo:** [https://logmind-ai.onrender.com](https://logmind-ai.onrender.com)

---

## ⚡ The "Wow" Factor (Key Features)

- **🚀 Instant Root Cause Analysis (RCA):** Converts cryptic stack traces into a human-readable narrative in milliseconds.
- **🛠️ Prescriptive Remediation:** Provides a **step-by-step fix**, acting as a virtual senior engineer to guide the developer.
- **📊 Intelligent Priority Mapping:** Automatically categorizes incidents (High, Medium, Low) based on system impact and severity.
- **☁️ Production-Ready Architecture:** A high-performance FastAPI backend serving a responsive, developer-centric frontend, deployed via **Infrastructure as Code (IaC)**.

---

## 🛠️ Tech Stack & Innovation

| Layer | Technology | Implementation Detail |
| :--- | :--- | :--- |
| **AI Engine** | `Google Gemini 1.5 Flash` | Primary engine for high-context reasoning and speed. |
| **Local AI** | `Ollama (Local LLM)` | Supports local execution for privacy-first, air-gapped analysis. |
| **Backend** | `FastAPI` | Asynchronous API handling ensuring low-latency responses. |
| **Hosting** | `Render` | Globally distributed hosting with automatic scaling. |
| **UI/UX** | `Custom Dev-Console` | Specialized dark-mode interface designed for high readability. |

---

## 🔒 Security & Configuration

### Secret Management
To ensure production-grade security, **LogMind AI** follows the **Principle of Least Privilege**:
- **Zero Hardcoding:** No API keys are stored in the source code.
- **Environment Isolation:** Sensitive credentials are managed via `.env` files (local) and **Render Environment Secrets** (production).
- **Git Protection:** A strict `.gitignore` policy prevents the leakage of credentials to public repositories.

### Required Configuration
The application requires the following environment variable to connect to the AI engine:
- `GEMINI_API_KEY`: Your Google AI Studio API Key.

---

## 💻 Developer Setup & Local Execution

If you wish to run a local instance for development purposes, follow these steps:

1. **Clone & Install**
   ```bash
   git clone https://github.com/your-username/logmind-ai.git
   cd backend && pip install -r requirements.txt
   ```
2. **Configure your AI "Brain" (Choose One):**
   - **Option A (Cloud):** Create a `.env` file in the `/backend` folder and add:
     `GEMINI_API_KEY=your_api_key_here`
   - **Option B (Private/Local):** Install [Ollama](https://ollama.com/) and run a local model (e.g., `ollama run gemma`). Update the backend configuration to point to the local Ollama endpoint.
3. **Launch Local Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   Access the local instance at: `http://localhost:8000`

---

## 📖 Example Workflow

**❌ The Pain (Raw Log):**
`2024-05-04 ERROR com.app.PaymentGateway - PSQLException: Connection refused. Connection to localhost:5432 refused.`

**✅ The Win (LogMind AI Insight):**
- **Priority:** 🔴 **HIGH**
- **Root Cause:** Database connectivity failure. The PostgreSQL service is either down or blocking requests on port 5432.
- **Fix:** 1. Check PG service status. 2. Verify `.env` DB_HOST. 3. Check firewall rules for port 5432.

---

## 🏆 Future Roadmap
- [ ] **Multi-Log Correlation:** Analyzing logs across multiple microservices to find distributed failures.
- [ ] **Auto-Ticketing:** Direct integration with Jira/GitHub Issues API for automated bug reporting.
- [ ] **Real-time Streaming:** Connecting to live log streams via ELK or Splunk for proactive alerting.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
