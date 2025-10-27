## Music Tracker

This is a web application for searching and tracking music albums, built with Python, Flask, and PostgreSQL.

This project is a port and modernization of an older application I built using Ruby and Sinatra. The goal was to demonstrate my ability to work with Python's web ecosystem, implement modern best practices like an ORM and Blueprints, and build a full-stack, portfolio-ready application.

---

### Features

* User registration and authentication (via Flask-Login and `passlib` for hashing).
* Search for albums by artist and title using the MusicBrainz API.
* Fetch cover art from the Cover Art Archive API.
* Save albums to a personal, paginated list.
* Add, Edit, and Delete albums from your list.

---

### Technology Stack

* **Backend:** Python 3.11+
* **Framework:** Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy (via Flask-SQLAlchemy)
* **Authentication:** Flask-Login
* **API Client:** `requests`
* **Testing:** `pytest`
* **Frontend:** Jinja2 templates with Bootstrap 5
* **Deployment:** Gunicorn & Render

---

### Local Development Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/python-music-tracker.git](https://github.com/your-username/python-music-tracker.git)
    cd python-music-tracker
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a PostgreSQL database (e.g., `createdb musictracker`).
5.  Create your `.env` file (copy `.env.example` if you make one) and add your `SECRET_KEY` and `DATABASE_URL`.
    ```
    SECRET_KEY='a-new-random-secret'
    DATABASE_URL='postgresql://your_user:your_password@localhost:5432/musictracker'
    ```
6.  Run the application:
    ```bash
    flask --app app run --debug
    ```
7.  The application will be running at `http://127.0.0.1:5000`.
