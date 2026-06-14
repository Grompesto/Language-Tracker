# Language-Tracker

A simple and efficient REST API for tracking vocabulary and managing language learning progress. Built with Python and FastAPI, this project implements core CRUD operations for word management and features a backend foundation for spaced repetition learning.

## 🚀 Features

- **Word Management (CRUD):** Add, view, filter, and delete words from your learning list.
- **Data Validation:** Strict type-checking and request validation powered by Pydantic.
- **Automated Documentation:** Interactive API playground available out-of-the-box via Swagger UI.
- **Spaced Repetition (In Progress):** Smart review intervals based on learning history to maximize memory retention.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Validation:** Pydantic
- **Server:** Uvicorn

## 📋 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/words` | Add a new word to the dictionary |
| `GET` | `/words/{word_id}` | Get details of a specific word by ID |
| `DELETE` | `/words/{word_id}` | Remove a word from the dictionary by ID |

## 🔧 Installation & Setup

Follow these steps to run the project locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Grompesto/Language-Tracker.git](https://github.com/Grompesto/Language-Tracker.git)
   cd Language-Tracker
2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
3. **Run the development server:**
   ```bash
   uvicorn main:app --reload
4. **Access the API:**
   *Live API: http://127.0.0.1:8000*
   *Interactive Swagger UI Docs: http://127.0.0.1:8000/docs*
