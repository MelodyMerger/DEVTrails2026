# 🛡️ Intelligent Fraud Detection in Parametric Insurance Using Sensor Fusion

**Team RYVEN** — Ankit Kumar · Aniket Krishnet · Sarthak Verma · Bhoomi Gupta · Bhawna Gupta

> *"We don't just ask where you are. We ask whether everything about your situation makes sense — and that's a much harder question to fake."*

---

## 📌 What is This Project?

Parametric insurance auto-pays delivery workers when real-world events (like heavy rain) occur. But GPS-only triggers can be exploited through spoofing apps. Our system detects fraud by cross-validating **6 independent signal layers** in real time — making it nearly impossible to fake a claim.

---

## 🚀 Live Demo

Open `frontend/index.html` in your browser after starting the backend.

Use the **"Load Genuine Claim"** or **"Load Fraudulent Claim"** buttons to see the system in action instantly.

---

## 🗂️ Project Structure

```
ryven-fraud-detection/
├── backend/
│   ├── main.py              # FastAPI app — all 6 detection layers
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Full web UI (no build step needed)
├── ml/
│   └── models.py            # ML model stubs (Random Forest, Isolation Forest, Graph)
└── README.md
```

---

## ⚙️ How to Run Locally

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ryven-fraud-detection.git
cd ryven-fraud-detection
```

### Step 2 — Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Start the backend
```bash
uvicorn main:app --reload
```

The API will be live at: `http://localhost:8000`

You can explore the interactive API docs at: `http://localhost:8000/docs`

### Step 4 — Open the frontend
Just open `frontend/index.html` in your browser. No build step, no npm, no setup.

Make sure the **Backend URL** field in the UI says `http://localhost:8000`.

---

## 🧠 How the Detection Works

When a claim arrives, it passes through 6 independent layers:

| Layer | What It Checks |
|---|---|
| **1. Sensor Fusion** | GPS vs Wi-Fi vs Cell tower — do they agree? |
| **2. Motion Analysis** | Accelerometer/gyroscope vs claimed movement |
| **3. Device Integrity** | Rooted device, mock location app, emulator, VPN |
| **4. Behavioral Analysis** | Claim frequency, speed, route consistency |
| **5. Weather Validation** | Claimed weather vs real weather API data |
| **6. Fraud Ring Detection** | Shared devices/IPs across multiple users |

All layers produce a risk score that feeds into a **weighted ensemble engine**:

| Trust Score | Decision |
|---|---|
| ✅ High (risk < 30%) | Instant payout approved |
| ⚠️ Medium (risk 30–65%) | Quick user verification requested |
| ❌ Low (risk > 65%) | Claim blocked, flagged for manual review |

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **ML:** Scikit-learn (Random Forest, Isolation Forest), NetworkX (graph analysis)
- **Frontend:** Vanilla HTML/CSS/JS (zero dependencies)
- **External APIs:** OpenWeatherMap (weather validation)
- **Sensors Used:** GPS, Accelerometer, Gyroscope, Wi-Fi, Cell Tower, IP Address

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/analyze` | Analyze a claim (main endpoint) |
| `GET` | `/demo/genuine` | Sample genuine claim payload |
| `GET` | `/demo/fraudulent` | Sample fraudulent claim payload |
| `GET` | `/docs` | Interactive Swagger UI |

---

## 🔮 What's Next

- Train ML models on real labeled datasets
- Add LSTM deep learning for sequential behavior analysis
- Integrate live OpenWeatherMap API calls
- On-device ML (edge processing) for better privacy
- Expand to crop insurance, travel, and ride-hailing use cases

---

## 📚 References

- DEV Community — AI-powered insurance systems
- Norton — GPS spoofing risks and detection
- Stanford Research — Anti-spoofing techniques
- Neo4j — Graph-based fraud detection
- PwC — AI in claims processing

---

*Guidewire DEVTrails University Hackathon · Phase 2 · 2025*
