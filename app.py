import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/')
def home():
    return jsonify({"message": "Flask is running on Render!"})

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    code = data.get("code", "")
    test_cases = data.get("testCases", [])

    if not code:
        return jsonify({"error": "Code is missing"}), 400
    if not test_cases:
        return jsonify({"error": "Test cases are missing"}), 400

    results = []
    for test_case in test_cases:
        input_data = test_case.get("input")
        expected_output = test_case.get("expectedOutput")
        if input_data is None or expected_output is None:
            results.append({"error": "Missing input or expectedOutput in test case"})
            continue

        try:
            exec_globals = {}
            exec(code, exec_globals)
            result = exec_globals["solution"](input_data)
            results.append({
                "input": input_data,
                "expectedOutput": expected_output,
                "result": str(result)
            })
        except Exception as e:
            results.append({
                "input": input_data,
                "expectedOutput": expected_output,
                "result": f"Error: {str(e)}"
            })

    response = jsonify({"results": results})
    response.headers.add("Access-Control-Allow-Origin", "*")  # Explicitly allow requests
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
