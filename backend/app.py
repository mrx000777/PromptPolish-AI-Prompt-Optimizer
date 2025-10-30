from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # frontend connection

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    user_prompt = data.get("prompt")
    optimized_prompt = f"Improved version of: {user_prompt}"  # placeholder logic
    return jsonify({"optimized_prompt": optimized_prompt})

if __name__ == "__main__":
    app.run(debug=True)
