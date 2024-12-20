import os
import sys

from flask import Flask, request, jsonify


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.debugger import PythonDebugger

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Metatron - Python Debugger"

@app.route('/debug', methods=['POST'])
def debug_code():
    code = request.json['code']
    #Initialize the debugger with the submitted code
    debugger = PythonDebugger(code)
    result = debugger.run_debugger()

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)  