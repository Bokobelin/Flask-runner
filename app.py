import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask is running on Render!"})

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()  # Ensure you're using get_json() to parse the request
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400  # Return 400 if JSON is invalid

    code = data.get("code", "")
    test_cases = data.get("testCases", [])

    if not code:
        return jsonify({"error": "Code is missing"}), 400  # Ensure code is present
    if not test_cases:
        return jsonify({"error": "Test cases are missing"}), 400  # Ensure test cases are present

    # Execute the code for each test case
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

    return jsonify({"results": results})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)