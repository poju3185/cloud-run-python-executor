# app/main.py
import os
import json
import logging
from flask import Flask, request, jsonify
from contextlib import redirect_stdout
import io

# 設定日誌
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_script():
    """
    接收 Python 腳本，在 Cloud Run 的沙箱中直接執行，並返回結果。
    """
    # 1. 基本輸入驗證
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
    
    # 2. 直接在記憶體中執行腳本
    stdout_capture = io.StringIO()
    try:
        # 建立一個臨時的 module scope
        script_scope = {}
        with redirect_stdout(stdout_capture):
            # 執行使用者提供的腳本字串
            exec(user_script_str, script_scope)
        
        # 從 scope 中取得 main 函式
        main_func = script_scope.get('main')
        if not callable(main_func):
             raise NameError("main() function not defined or not callable in the script")

        # 執行 main 函式並獲取結果
        result = main_func()
        
        # 驗證回傳值是否為 JSON 可序列化
        json.dumps(result)
        output_data['result'] = result

    except Exception as e:
        # 捕獲執行過程中的任何錯誤
        output_data['error'] = f"{type(e).__name__}: {e}"

    finally:
        # 收集 stdout
        output_data['stdout'] = stdout_capture.getvalue()

    # 3. 返回結果
    if output_data.get("error"):
        return jsonify({"error": output_data["error"], "stdout": output_data["stdout"]}), 400

    return jsonify({
        "result": output_data.get("result"),
        "stdout": output_data.get("stdout")
    }), 200

if __name__ == '__main__':
    # 在本地開發時，使用 Flask 內建的 server
    # 在 Cloud Run 上，會由 Gunicorn 啟動
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
