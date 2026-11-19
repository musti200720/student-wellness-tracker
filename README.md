# 🌿 Student Wellness Tracker

A health and lifestyle monitoring web application for college students.
Students can log their daily sleep, water intake, exercise and mood, get a
wellness score with recommended steps, and track their progress on a dashboard.

> Built as a TY BSc IT project using Python Flask, MySQL, HTML, CSS and JavaScript.

---

## ✨ Features

- User registration and login (passwords stored as secure hashes)
- Daily check-in for sleep, water, exercise and mood
- Wellness score out of 100 with personalised recommended steps
- Check-in history with a score for each entry and delete option
- Dashboard with averages and charts of the last 7 check-ins
- Each user sees only their own data
- Form validation in both JavaScript and Flask
- Responsive, modern design with a custom 404 page

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Front end | HTML, CSS, JavaScript, Chart.js |
| Back end | Python, Flask, Jinja2 |
| Database | MySQL |
| Security | Werkzeug password hashing, Flask sessions |

---

## 📁 Project Structure

```
student_wellness_tracker/
├── app.py                 # Flask routes and application logic
├── recommender.py         # Wellness score and suggestion rules
├── config.example.py      # Example settings (copy to config.py)
├── database.sql           # MySQL tables
├── requirements.txt       # Python libraries
├── templates/             # HTML templates (Jinja2)
└── static/
    ├── css/style.css
    └── js/                # script.js, dashboard.js
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3
- MySQL Server (and optionally MySQL Workbench)
- Git

### 2. Clone the repository
```
git clone https://github.com/musti200720/student-wellness-tracker.git
cd student-wellness-tracker
```

### 3. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### 4. Install the libraries
```
pip install -r requirements.txt
```

### 5. Set up the database
Open MySQL (Workbench or the command line) and run the script in `database.sql`.

### 6. Add your settings
Copy `config.example.py` to a new file named `config.py`, then enter your own
MySQL password and a random secret key.

### 7. Run the app
```
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 📖 How It Works

1. Register an account and log in.
2. Fill in the daily check-in form.
3. Flask validates the data and saves it to MySQL.
4. The recommender calculates a wellness score and creates suggestions based on
   the check-in values.
5. View your history and dashboard to track your progress.

---

## 🔜 Coming Soon

- 🤖 **AI-powered personalised suggestions** (the current suggestion system is
  rule-based)
- 🗄️ **Hosted online database connection and deployment**
- 📈 Weekly and monthly progress reports
- 🔔 Reminders and goal setting

---

## ⚠️ Disclaimer

The suggestions in this app are general wellness tips for educational purposes.
They are not medical advice. Please consult a doctor for any health concerns.

---

## 👤 Author

**Mustansir** – TY BSc IT student
GitHub: [@musti200720](https://github.com/musti200720)
