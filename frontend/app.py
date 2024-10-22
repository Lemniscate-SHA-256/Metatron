from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Metatron - Python Debugger"

@app.route('/debug', methods=['POST'])
def debug_code():
    code = request.json['code']
    # For now, just log the code or use subprocess to call backend debugger
    with open("code_to_debug.py", "w") as f:
        f.write(code)

    result = subprocess.run(["python3", "code_to_debug.py"], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

if __name__ == '__main__':
    app.run(debug=True)  