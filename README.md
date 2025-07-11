# 🩺 AI-Powered Symptom Analyzer and Doctor Recommender

A Flask-based web application that uses Google's Gemini AI to analyze patient symptoms and intelligently recommend the most relevant medical specialization. Once the specialization is identified, the system fetches a list of matching doctors from the Supabase backend.

---

## 🚀 Features

- 🌟 **AI-Powered Diagnosis** using Google Gemini (`gemini-1.5-flash`)
- 🧠 Extracts **medical specialization** from natural language symptoms
- ✅ Returns **confidence level** and **reasoning**
- 🧑‍⚕️ Retrieves **matching doctors** from **Supabase database**
- 🔐 Fully secured via **.env configuration**
- 🌐 CORS-enabled REST API
- 📦 JSON-formatted API responses

---

## 🛠 Tech Stack

| Layer          | Technology        |
|----------------|-------------------|
| Backend        | Flask (Python)     |
| AI Integration | Gemini (Google Generative AI) |
| Database       | Supabase (PostgreSQL backend) |
| Environment    | Python-dotenv      |
| API Handling   | Flask REST + CORS  |
| Deployment     | Compatible with Render / Vercel / Railway / Heroku |

---

## 📂 Project Structure
