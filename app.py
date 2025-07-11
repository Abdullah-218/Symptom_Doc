import os
import json
import re
import google.generativeai as genai
from supabase import create_client, Client
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Supabase Configuration
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Flask App Configuration
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_json_from_response(response_text):
    """
    Attempt to extract JSON from the response text
    """
    # Try to find JSON-like content between { and }
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    
    if json_match:
        try:
            # Remove any code block markers
            json_str = json_match.group(0).replace('```json', '').replace('```', '').strip()
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Could not parse JSON. Attempting manual parsing.")
    
    # Manual parsing if regex fails
    specialization_match = re.search(r'"specialization"\s*:\s*"([^"]+)"', response_text)
    confidence_match = re.search(r'"confidence"\s*:\s*"([^"]+)"', response_text)
    reasoning_match = re.search(r'"reasoning"\s*:\s*"([^"]+)"', response_text)
    
    return {
        "specialization": specialization_match.group(1) if specialization_match else "General Medicine",
        "confidence": confidence_match.group(1) if confidence_match else "medium",
        "reasoning": reasoning_match.group(1) if reasoning_match else "Unable to extract specific specialization"
    }

def analyze_symptoms(symptoms: str):
    """
    Analyze symptoms using Gemini API and find matching doctors in Supabase
    """
    # Enhanced prompt with more specific guidance
    prompt = f"""
    You are a medical diagnostic AI. Carefully analyze the following symptoms and determine the most appropriate medical specialization.

    Patient Symptoms: '{symptoms}'

    Your task:
    1. Identify the most likely medical specialization needed
    2. Provide a confidence level
    3. Give a brief reasoning for your recommendation

    Respond STRICTLY in this JSON format:
    {{
        "specialization": "Exact medical specialization (e.g., Cardiology, Neurology, General Medicine)",
        "confidence": "high/medium/low",
        "reasoning": "Concise explanation of how symptoms relate to the specialization"
    }}

    Key Specializations to Consider:
    - Cardiology (heart-related)
    - Neurology (nerve, brain issues)
    - Pulmonology (lung, breathing)
    - Gastroenterology (digestive system)
    - Endocrinology (hormonal)
    - Dermatology (skin)
    - Psychiatry (mental health)
    - Rheumatology (joints, autoimmune)
    - Urology (urinary system)
    - Ophthalmology (eye care)
    - Obstetrics/Gynecology
    - Pediatrics (children's health)
    - Geriatrics (elderly care)
    - Orthopedics (bone, muscle)
    - General Medicine (when symptoms are non-specific)
    - Infectious Disease
    - Oncology
    """
    
    try:
        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        # Extract and parse the JSON
        try:
            analysis = extract_json_from_response(response.text)
        except Exception as json_error:
            print(f"JSON Extraction Error: {json_error}")
            analysis = {
                "specialization": "General Medicine",
                "confidence": "medium",
                "reasoning": "Unable to extract specific specialization"
            }
        
        # Query Supabase for doctors matching the specialization
        doctors_response = supabase.table("doctors").select("*").eq("specialization", analysis['specialization']).execute()
        
        return {
            "analysis": analysis,
            "doctors": doctors_response.data or []
        }
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/analyze-symptoms', methods=['POST'])
def symptoms_analysis():
    """
    API endpoint for symptom analysis
    """
    try:
        # Get symptoms from JSON request
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()
        
        # Validate input
        if not symptoms:
            return jsonify({
                "error": "Please provide a valid symptom description",
                "status": "error"
            }), 400
        
        # Analyze symptoms
        result = analyze_symptoms(symptoms)
        
        if result:
            return jsonify({
                "status": "success",
                "analysis": result['analysis'],
                "doctors": result['doctors']
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Unable to process symptoms"
            }), 500
    
    except Exception as e:
        print(f"Error in symptoms analysis: {e}")
        return jsonify({
            "status": "error", 
            "message": "An unexpected error occurred"
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error handler
    """
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

if __name__ == '__main__':
    # Use debug mode during development
    app.run(debug=True)