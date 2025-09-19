# Student At-Risk Early Warning Dashboard

A **rule-based and ML-enhanced** dashboard that merges attendance, assessment, and fee data to proactively identify at-risk students. Built with open-source technologies, it empowers educators to intervene early, reducing drop-out rates without heavy budgets or black-box algorithms.

***

## 🔍 Project Overview

Many institutes store student attendance, test scores, and fee records in separate spreadsheets—missing the chance to spot warning signs until final results. This project:

- **Consolidates** data from multiple sources  
- **Cleans** and **validates** inputs automatically  
- **Engineers** features (attendance %, grade trends, failed-attempt ratios)  
- **Scores** risk with transparent rules and optional ML models  
- **Visualizes** results in an intuitive, color-coded dashboard  
- **Sends** automated email/SMS alerts to mentors & counselors  

***

## ⚙️ Features

- Data Ingestion: CSV/Excel upload API with schema validation  
- ETL Pipeline: Duplicate removal, format standardization  
- Feature Engineering: Attendance velocity, grade trend analysis  
- Risk Assessment:  
  - Rule-based thresholds (e.g., <75% attendance)  
  - Optional ML classifiers (Random Forest, Naive Bayes)  
- Dashboard:  
  - React front-end with interactive charts  
  - Real-time updates via WebSocket/React Query  
- Notifications: Email and SMS alerts powered by Celery & Twilio  
- Backup & Audit: Nightly database backups and change logs  

***

## 🛠️ Tech Stack

| Layer                   | Technologies                                          |
|-------------------------|-------------------------------------------------------|
| Frontend                | React.js, TypeScript, Material-UI, Chart.js, Redux    |
| Backend/API             | Python (FastAPI/Flask), PostgreSQL, SQLAlchemy        |
| ML & Data Processing    | pandas, scikit-learn, joblib, Apache Airflow          |
| Task Queue              | Celery, Redis                                         |
| Notifications           | SMTP (SendGrid), Twilio SMS                           |
| DevOps & Infrastructure | Docker, GitHub Actions, AWS/GCP, Prometheus, Grafana  |

***

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose  
- Python 3.9+ & Node.js 16+  
- AWS/GCP account (for production) or local environment  

### Clone & Install

```bash
git clone https://github.com/your-org/at-risk-dashboard.git
cd at-risk-dashboard
```

#### Backend

```bash
cd backend
cp .env.example .env
# Fill in DB credentials, Twilio API keys, SMTP settings
docker-compose up -d postgres redis
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
cp .env.example .env
# Fill in API_BASE_URL
npm install
npm start
```

***

## 📊 Usage

1. **Upload** attendance, grade, and fee files via the web UI or API.  
2. **Verify** data ingest status in the “Data Monitoring” tab.  
3. **Review** the Risk Dashboard—students are color-coded (Green/Yellow/Red).  
4. **Drill down** to individual student profiles for detailed metrics.  
5. **Configure** alert thresholds or toggle ML scoring in Settings.  
6. **Receive** automatic Mentor/Counselor notifications for Red-flagged students.

***

## 🔧 Configuration

All settings are managed via `.env` files:

- `API_BASE_URL` – Frontend API endpoint  
- `DATABASE_URL` – PostgreSQL connection string  
- `TWILIO_SID`, `TWILIO_TOKEN`, `TWILIO_FROM` – SMS alerts  
- `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` – Email alerts

***

## 📈 Roadmap

- [ ] Role-based access controls (Admin, Counselor, Mentor)  
- [ ] Historical trend analysis & reporting  
- [ ] Mobile-friendly PWA support  
- [ ] Plug-in architecture for new data sources  
- [ ] Advanced ML models (XGBoost, AutoML pipelines)

***

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/xyz`)  
3. Commit your changes (`git commit -m "Add xyz"`)  
4. Push to branch (`git push origin feature/xyz`)  
5. Open a Pull Request  

Please follow our [Coding Guidelines](docs/CODING.md) and ensure tests pass.

***

## 📝 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
