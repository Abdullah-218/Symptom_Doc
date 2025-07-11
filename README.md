# 🩺 AI-Powered Symptom Analyzer and Doctor Recommender

A Flask-based web application that uses Google's Gemini AI to analyze patient symptoms and intelligently recommend the most relevant medical specialization. Once the specialization is identified, the system fetches a list of matching doctors from the Supabase backend.

---

## 🚀 Features

-  **AI-Powered Diagnosis** using Google Gemini (`gemini-1.5-flash`)
-  Extracts **medical specialization** from natural language symptoms
-  Returns **confidence level** and **reasoning**
-  Retrieves **matching doctors** from **Supabase database**
-  Fully secured via **.env configuration**
-  CORS-enabled REST API
-  JSON-formatted API responses

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

```
project/
│
├── app.py                 # Main Flask server with API endpoints
├── templates/
│   └── index.html         # (Optional) Frontend template for symptom input
├── .env                   # Environment secrets (not pushed to GitHub)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```
---

## 🔐 Environment Variables

Create a `.env` file in the root of the project with the following:

```
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_role_key
```

📦 Installation & Running Locally

1. Clone the repo
```
git clone https://github.com/your-username/ai-symptom-analyzer.git
cd ai-symptom-analyzer
```
2. Set up Python environment
```
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# OR
venv\Scripts\activate     # For Windows
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create .env file and fill in credentials
 
(Refer to the Environment Variables section above)

5. Run the Flask app
```
python app.py
```

🧪 API Endpoint

POST /analyze-symptoms

Request Body:
```
{
  "symptoms": "chest pain and shortness of breath"
}
```

Response: 
```
{
  "status": "success",
  "analysis": {
    "specialization": "Cardiology",
    "confidence": "high",
    "reasoning": "Symptoms indicate a possible cardiac condition"
  },
  "doctors": [
    {
      "id": 1,
      "name": "Dr. A. Kumar",
      "specialization": "Cardiology",
      ...
    }
  ]
}
```

🧠 How It Works

1. User submits symptoms via API or frontend.
2. Gemini AI processes the prompt and returns:
      •	Medical specialization
      •	Confidence level
      •	Reasoning
3. Supabase is queried for doctors with matching specialization.
4. JSON response returned to the client.

⸻

📌 Future Enhancements:
• ✅ Add user authentication (JWT/OTP)
• 📅 Appointment scheduling with available doctors
• 📃 Medical history tracking for patients
• 🤖 AI-powered treatment suggestions
• 🩻 Symptom-image analysis (skin rashes, X-rays)

 ____

 
