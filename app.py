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

    try:
        exec_globals = {}
        exec(code, exec_globals)
        return jsonify({"output": str(exec_globals)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
