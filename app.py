import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask is running on Render!"})

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "No code provided!"}), 400

    try:
        # Safe execution using a sandboxed environment
        exec_globals = {"__builtins__": {}}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)

        # Capture and return the output from locals if any
        output = exec_locals if exec_locals else {"message": "Code executed successfully"}
        return jsonify({"output": output})

    except Exception as e:
        # Returning more specific error message
        return jsonify({"error": f"Error while executing code: {str(e)}"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    