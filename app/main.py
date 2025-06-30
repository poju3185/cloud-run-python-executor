# app/main.py
import os
import json
import logging
from flask import Flask, request, jsonify
from contextlib import redirect_stdout
import io

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_script():
    """
    Execute Python script directly in Cloud Run sandbox and return results.
    """
    # 1. Basic input validation
    try:
        req_data = request.get_json()
        if not req_data or 'script' not in req_data:
            return jsonify({"error": "Invalid input: 'script' key is required."}), 400
        
        user_script_str = req_data['script']
        if not isinstance(user_script_str, str) or "def main():" not in user_script_str:
            return jsonify({"error": "Script must be a string and contain a 'main()' function."}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format."}), 400

    output_data = {
        "result": None,
        "stdout": "",
        "error": None
    }
    
    # 2. Execute script directly in memory
    stdout_capture = io.StringIO()
    try:
        # Create a temporary module scope
        script_scope = {}
        with redirect_stdout(stdout_capture):
            # Execute user-provided script string
            exec(user_script_str, script_scope)
        
        # Get main function from scope
        main_func = script_scope.get('main')
        if not callable(main_func):
             raise NameError("main() function not defined or not callable in the script")

        # Execute main function and get result
        result = main_func()
        
        # Verify return value is JSON serializable
        json.dumps(result)
        output_data['result'] = result

    except Exception as e:
        # Catch any errors during execution
        output_data['error'] = f"{type(e).__name__}: {e}"

    finally:
        # Collect stdout
        output_data['stdout'] = stdout_capture.getvalue()

    # 3. Return results
    if output_data.get("error"):
        return jsonify({"error": output_data["error"], "stdout": output_data["stdout"]}), 400

    return jsonify({
        "result": output_data.get("result"),
        "stdout": output_data.get("stdout")
    }), 200

if __name__ == '__main__':
    # For local development, use Flask's built-in server
    # On Cloud Run, it will be started by Gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
