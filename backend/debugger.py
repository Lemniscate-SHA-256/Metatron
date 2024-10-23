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
            #Dynamically create and run the script within the debugger
            exec(self.script, {'pdb':pdb})
        except Exception as e:
            logging.error(f"Error occured : {e}")
            return str(e)
        return "Debugging Completed Succesfully"

#Test script to debug
if __name__ == "__main__":
    script = """
def test_function():
    x = 10
    y = 20
    z  = x + y
    print(f"Result: {z}")
    pdb.set_trace() #setting a breakpoint here
    return z

test _function()   
"""
    debugger = PythonDebugger(script)
    debugger.run_debugger()

