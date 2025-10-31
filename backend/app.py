from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
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

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Improve this prompt for better AI output: {user_prompt}")

        # Print raw response for debugging
        print("\n========== RAW GEMINI RESPONSE ==========")
        print(response)
        print("=========================================\n")

        # Universal extraction logic
        optimized_prompt = ""

        # Case 1: Direct text (most common)
        if getattr(response, "text", None):
            optimized_prompt = response.text.strip()

        # Case 2: Candidate-based response
        elif getattr(response, "candidates", None):
            for candidate in response.candidates:
                if getattr(candidate, "content", None):
                    for part in getattr(candidate.content, "parts", []):
                        if getattr(part, "text", None):
                            optimized_prompt += part.text.strip() + " "

        # Case 3: Safety fallback (convert to string if needed)
        if not optimized_prompt.strip():
            optimized_prompt = str(response).strip()

        # Clean fallback
        if not optimized_prompt or optimized_prompt.lower().startswith("<response"):
            optimized_prompt = "Unable to generate optimized prompt."

        return jsonify({"optimized_prompt": optimized_prompt.strip()})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
