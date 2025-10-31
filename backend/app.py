from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    user_prompt = data.get("prompt")

    # Use Gemini model to optimize prompt
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(f"Improve this prompt for better AI output: {user_prompt}")

    optimized_prompt = response.text.strip()
    return jsonify({"optimized_prompt": optimized_prompt})

if __name__ == "__main__":
    app.run(debug=True)
