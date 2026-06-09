# AI-Powered Real-Time Finance Tracker & Forecaster
A full-stack, production-grade personal finance dashboard built with **Django** and **Tailwind CSS**. This application goes beyond basic expense tracking by integrating **Scikit-Learn** for predictive budget forecasting and the **Google Gemini API** for delivering automated, real-time financial audits.
---
## 🚀 Core Features
* **Dynamic Data Analytics:** An interactive dashboard tracking cash flow with functional live filtering across custom monthly and yearly timeframes using **Chart.js**.
* **Predictive Forecasting Engine:** A built-in **Scikit-Learn Linear Regression pipeline** that analyzes daily historical spending habits to mathematically project budget trend lines out to the end of the active month.
* **AI Real-Time Audit:** Direct integration with the **Google Gemini API** acting as a strict, zero-sugar-coating financial auditor, parsing user metrics instantly to deliver blunt, actionable risk assessments.
* **Production Ready Architecture:** Secure environment variable isolation, error handling, defensive UI fallbacks, and multi-user authentication, optimized for zero-downtime deployment on **Vercel**.
---
## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Django (Python) |
| **Database** | SQLite (Local) / PostgreSQL compatibility |
| **Machine Learning** | Scikit-Learn, NumPy |
| **Generative AI** | Google Generative AI SDK (Gemini Core) |
| **Frontend Rendering** | Chart.js, Tailwind CSS, HTML5 |
| **Deployment Platform** | Vercel |

---
## 📋 Local Setup & Installation
### 1. Clone the Repository
Bash
git clone https://github.com/mozo001/AI-Finance-Treacker.git 

##2. Set Up a Virtual Environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in your root project directory (where manage.py is located) and add your private credentials:

Code snippet
SECRET_KEY=your_django_secret_key_here
DEBUG=True
GEMINI_API_KEY=your_google_gemini_api_key_here
5. Run Database Migrations
Bash
python manage.py makemigrations
python manage.py migrate
6. Start the Development Server
Bash
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/ to test the application.

🧠 Machine Learning & Data Pipeline Architecture
Aggregation Layer: The Django ORM processes daily user database entries via ExtractDay and Sum aggregations, packaging them into structured arrays.

Trend Line Prediction: The backend feeds active coordinate pairs into a Scikit-Learn LinearRegression model object to calculate intercept data vectors.

Frontend Ingestion: The generated predictive arrays are safely pushed into the UI via custom JSON context serialization pipelines.

Dashed Visualization: Chart.js handles the parsed coordinates, overlaying a translucent bar structure for real historical data alongside a crisp, purple dashed line indicating the future trajectory.

🛡️ Production Deployment Note
This application is fully pre-configured to build on Vercel utilizing a custom vercel.json routing matrix combined with explicit WSGI entry points. When moving to production, ensure that your Vercel deployment project settings mirror the environment keys specified inside your local configuration.
