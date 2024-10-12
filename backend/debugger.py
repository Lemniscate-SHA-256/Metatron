import pdb
import logging

#Setup logging to track debugging sessions

logging.basicConfig(filename='logs/debug.log', level=logging.INFO)

class PythonDebugger:
    def __init__(self, script):
        self.script = script

    def run_debugger(self):
        try:
            logging.info(f"Starting debug session for {self.script}")
            pdb.run(self.script)
        except Exception as e:
            logging.error(f"Error occured : {e}")
            print(f"Error while debugging : {e}")

#Test script to debug
if __name__ == "__main__":
    script = """
def test_function():
    x = 10
    y = 20
    z  = x + y
    return z

test _function()   
"""
    debugger = PythonDebugger(script)
    debugger.run_debugger()

