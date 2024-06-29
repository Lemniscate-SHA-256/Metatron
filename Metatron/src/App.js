import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState('');

  const handleAnalyze = async () => {
    const response = await axios.post('http://localhost:5000/analyze', { code });
    setResult(response.data.results);
  };

  const handleDebug = async () => {
    const response = await axios.post('http://localhost:5000/debug', { code });
    setResult(response.data.results);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Metatron Code Debugger</h1>
      </header>
      <main>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code here..."
          rows="20"
          cols="80"
        ></textarea>
        <div>
          <button onClick={handleAnalyze}>Analyze Code</button>
          <button onClick={handleDebug}>Start Debugging</button>
        </div>
        <pre>{result}</pre>
      </main>
    </div>
  );
}

export default App;
