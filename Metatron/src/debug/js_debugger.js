const { exec } = require('child_process');

class JSDebugger {
    static analyze(file) {
      exec(`eslint ${file}`, (error, stdout, stderr) => {
        if (error) {
          console.log("ESLint Errors:\n", stdout);
          return;
        }
        console.log("No issues found.");
      });
    }
  }
  
  // Example usage (remove in production)
  JSDebugger.analyze(process.argv[2] || 'test.js');