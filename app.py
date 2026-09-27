from flask import Flask, render_template, request, session , redirect
import os
import sqlite3

from utils.resume_parser import extract_text
from utils.analyzer import analyze_resume, match_job
from utils.ai_analyzer import generate_ai_analysis

app = Flask(__name__)
app.secret_key = "ai-resume-analyzer-secret-key"

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_name TEXT,
            ats_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)",
            (full_name, email, password)
        )

        conn.commit()
        conn.close()

        return "Account created successfully!"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect("/dashboard")
            return render_template(
    "login.html",
    error="Invalid email or password!"
)

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return "Please login first!"

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name")
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT resume_name, ats_score, created_at
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    history_data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history_data
    )

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT full_name, email FROM users WHERE id = ?",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "user_id" not in session:
        return redirect("/login")

    file = request.files["resume"]

    if file:

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, file.filename)

        # Save resume
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)
        session["resume_text"] = resume_text
        analysis = analyze_resume(resume_text)
        ai_analysis = generate_ai_analysis(resume_text)


        # Save analysis history
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO analysis_history
            (user_id, resume_name, ats_score)
            VALUES (?, ?, ?)
            """,
            (
                session["user_id"],
                file.filename,
                analysis["score"]
            )
        )

        conn.commit()
        conn.close()

        

        # Show extracted text
        return render_template(
    "result.html",
    analysis=analysis,
    ai_analysis=ai_analysis
)

    return "No file selected"

@app.route("/job-match", methods=["POST"])
def job_match():

    job_description = request.form["job_description"]

    resume_text = session.get("resume_text", "")

    analysis = match_job(
        resume_text,
        job_description
    )

    return render_template(
    "job_result.html",
    analysis=analysis
)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)