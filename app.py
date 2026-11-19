from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import config
from recommender import calculate_score, get_rating, get_suggestions

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )


# ---------- Public pages ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------- Register / Login / Logout ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if len(password) < 6:
            return render_template("register.html",
                                   error="Password must be at least 6 characters.",
                                   full_name=full_name, email=email)
        if password != confirm_password:
            return render_template("register.html",
                                   error="Passwords do not match.",
                                   full_name=full_name, email=email)

        password_hash = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template("register.html",
                                       error="This email is already registered.",
                                       full_name=full_name, email=email)

            cursor.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                (full_name, email, password_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Database error:", err)
            return render_template("register.html",
                                   error="Something went wrong. Please try again.",
                                   full_name=full_name, email=email)

        return render_template("register.html",
                               success="Account created successfully!")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Database error:", err)
            return render_template("login.html",
                                   error="Something went wrong. Please try again.")

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            return redirect(url_for("dashboard"))

        return render_template("login.html",
                               error="Invalid email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Check-in and suggestions ----------

@app.route("/checkin")
def checkin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("checkin.html")


@app.route("/result", methods=["POST"])
def result():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Server-side validation
    try:
        sleep = float(request.form["sleep"])
        water = int(request.form["water"])
        exercise = int(request.form["exercise"])
    except (ValueError, KeyError):
        return render_template("checkin.html",
                               error="Please enter valid numbers in all fields.")

    mood = request.form.get("mood", "")
    valid_moods = ["Happy", "Calm", "Tired", "Stressed"]

    if not (0 <= sleep <= 24):
        return render_template("checkin.html",
                               error="Sleep hours must be between 0 and 24.")
    if not (0 <= water <= 30):
        return render_template("checkin.html",
                               error="Water glasses must be between 0 and 30.")
    if not (0 <= exercise <= 600):
        return render_template("checkin.html",
                               error="Exercise minutes must be between 0 and 600.")
    if mood not in valid_moods:
        return render_template("checkin.html",
                               error="Please choose how you are feeling.")

    # Save the check-in for the logged-in user
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO checkins
                 (user_id, sleep_hours, water_glasses, exercise_minutes, mood)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (session["user_id"], sleep, water, exercise, mood))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)
        return render_template("checkin.html",
                               error="Could not save your check-in. Please try again.")

    # Redirect to the suggestions page for this check-in
    return redirect(url_for("suggestions", checkin_id=new_id))


@app.route("/suggestions/<int:checkin_id>")
def suggestions(checkin_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    row = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM checkins WHERE id = %s AND user_id = %s",
            (checkin_id, session["user_id"])
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)

    if row is None:
        return render_template("404.html"), 404

    sleep = float(row["sleep_hours"])
    water = row["water_glasses"]
    exercise = row["exercise_minutes"]
    mood = row["mood"]

    score = calculate_score(sleep, water, exercise, mood)
    rating = get_rating(score)
    tips = get_suggestions(sleep, water, exercise, mood)

    return render_template("suggestions.html", checkin=row, score=score,
                           rating=rating, tips=tips)


# ---------- History and delete ----------

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    checkins = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM checkins WHERE user_id = %s ORDER BY id DESC",
            (session["user_id"],)
        )
        checkins = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)

    # Add a wellness score to each row
    for row in checkins:
        score = calculate_score(float(row["sleep_hours"]), row["water_glasses"],
                                row["exercise_minutes"], row["mood"])
        row["score"] = score
        row["css"] = get_rating(score)["css"]

    return render_template("history.html", checkins=checkins)


@app.route("/delete/<int:checkin_id>", methods=["POST"])
def delete_checkin(checkin_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM checkins WHERE id = %s AND user_id = %s",
            (checkin_id, session["user_id"])
        )
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)

    return redirect(url_for("history"))


# ---------- Dashboard ----------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    stats = {"total": 0, "avg_sleep": 0, "avg_water": 0, "avg_exercise": 0}
    labels = []
    sleep_data = []
    water_data = []
    exercise_data = []
    latest = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """SELECT COUNT(*) AS total,
                      AVG(sleep_hours) AS avg_sleep,
                      AVG(water_glasses) AS avg_water,
                      AVG(exercise_minutes) AS avg_exercise
               FROM checkins WHERE user_id = %s""",
            (session["user_id"],)
        )
        row = cursor.fetchone()
        if row["total"] > 0:
            stats["total"] = row["total"]
            stats["avg_sleep"] = round(float(row["avg_sleep"]), 1)
            stats["avg_water"] = round(float(row["avg_water"]), 1)
            stats["avg_exercise"] = round(float(row["avg_exercise"]), 1)

        cursor.execute(
            "SELECT * FROM checkins WHERE user_id = %s ORDER BY id DESC LIMIT 7",
            (session["user_id"],)
        )
        recent = cursor.fetchall()
        recent.reverse()

        for r in recent:
            labels.append(r["created_at"].strftime("%d %b"))
            sleep_data.append(float(r["sleep_hours"]))
            water_data.append(r["water_glasses"])
            exercise_data.append(r["exercise_minutes"])

        # Wellness score of the most recent check-in
        if recent:
            last = recent[-1]
            score = calculate_score(float(last["sleep_hours"]), last["water_glasses"],
                                    last["exercise_minutes"], last["mood"])
            rating = get_rating(score)
            latest = {"id": last["id"], "score": score,
                      "label": rating["label"], "css": rating["css"]}

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Database error:", err)

    return render_template("dashboard.html", stats=stats, labels=labels,
                           sleep_data=sleep_data, water_data=water_data,
                           exercise_data=exercise_data, latest=latest)


# ---------- Error page ----------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)