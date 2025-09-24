import os
import google.generativeai as genai
# render_template-ஐ இம்போர்ட் செய்யவும்
from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # புதிய 'gemini-1.5-pro-latest' மாடலைப் பயன்படுத்தவும்
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    print("Gemini 1.5 Pro model configured successfully!")
except Exception as e:
    print(f"Error: {e}")

# === புதியதாக சேர்க்கப்பட்ட பகுதி START ===
@app.route('/')
def home():
    # templates ஃபோல்டரில் உள்ள index.html கோப்பை காண்பிக்கும்
    return render_template('index.html') 
# === புதியதாக சேர்க்கப்பட்ட பகுதி END ===

@app.route('/generate', methods=['POST'])
def generate_questions():
    if not model:
        return jsonify({"error": "Gemini API is not configured correctly. Check your API key."}), 500
    
    data = request.get_json()
    topic = data.get('topic')
    num_questions = data.get('num_questions')

    if not topic or not num_questions:
        return jsonify({"error": "Topic and number of questions are required."}), 400

    prompt = f"""
    Generate {num_questions} multiple-choice questions about "{topic}".
    For each question, provide four options (a, b, c, d).
    Clearly indicate the correct answer after the options.
    Separate each complete question block with '---'.

    Use this exact format for each question:

    [Question Number]. [Question Text]?
    a) [Option A]
    b) [Option B]
    c) [Option C]
    d) [Option D]
    Correct Answer: [Correct Letter]) [Correct Answer Text]

    ---
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"questions": response.text})
    except Exception as e:
        return jsonify({"error": f"An error occurred while generating questions: {e}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)