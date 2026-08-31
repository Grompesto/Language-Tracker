# Lexora (Language-Tracker) 🌍📖

Lexora is a smart, full-stack vocabulary building application designed to help users memorize new words efficiently. It features a custom RESTful API, secure JWT-based authentication, and an intelligent quiz system based on Spaced Repetition (SRS).

## ✨ Features

* **Smart Quizzes (Spaced Repetition System):** The application calculates the optimal time to review a word using an algorithm based on an `ease_factor` and a `next_review` timestamp.[cite: 26]
* **Secure Authentication:** Implements robust two-step JWT authentication using both Access and Refresh tokens for a seamless user experience.[cite: 18]
* **Full CRUD Operations:** Users can easily add, edit, delete, and browse their personal vocabulary lists.[cite: 17]
* **Responsive Frontend:** A lightweight, fast, and responsive Single Page Application (SPA) built with Vanilla JavaScript.[cite: 17]
* **Automated Testing:** Core functionalities (authentication and CRUD operations) are heavily tested using Pytest.[cite: 19, 20, 21]

## 🛠️ Tech Stack

**Backend:**
* [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for building the API.
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interactions.[cite: 24]
* [SQLite](https://www.sqlite.org/) - Lightweight database for storing user and vocabulary data.[cite: 24]
* [Passlib] & [python-jose] - For password hashing and JWT token generation.[cite: 18]

**Frontend:**
* HTML5, CSS3, Vanilla JavaScript (Fetch API).[cite: 17]

**Testing:**
* [Pytest](https://docs.pytest.org/) with an isolated in-memory SQLite database.[cite: 19]

## 🚀 How to Run Locally

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/Grompesto/Language-Tracker.git
cd Language-Tracker
\`\`\`

### 2. Set up the Python Virtual Environment
\`\`\`bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your secure settings:
\`\`\`env
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
\`\`\`

### 5. Run the Application
Start the FastAPI server using Uvicorn:
\`\`\`bash
uvicorn main:app --reload
\`\`\`
The backend will be available at `http://127.0.0.1:8000`. You can explore the interactive API documentation at `http://127.0.0.1:8000/docs`.

### 6. Open the Frontend
Simply open the `index.html` file in your favorite browser, or use a tool like Live Server in VS Code to view the application.

## 🧪 Running Tests
To run the automated test suite, simply execute:
\`\`\`bash
pytest
\`\`\`

## 🐳 Running with Docker Compose

If you have Docker installed, you can spin up the entire application (Backend + Nginx Frontend) with a single command:

\`\`\`bash
docker-compose up --build
\`\`\`

* **Frontend (Nginx):** Available at `http://localhost` (Port 80)
* **Backend API:** Available at `http://localhost:8000`
* **Swagger Docs:** Available at `http://localhost:8000/docs`
