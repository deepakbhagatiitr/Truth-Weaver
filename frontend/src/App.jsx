

import React, { useState } from 'react';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Placeholder: Replace with actual backend endpoints
  // const BACKEND_URL = 'http://localhost:5000';

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
    setTranscript('');
    setAnalysis(null);
    setError('');
  };

  const handleUpload = async () => {
    if (!audioFile) {
      setError('Please select an audio file.');
      return;
    }
    setLoading(true);
    setError('');
    setTranscript('');
    setAnalysis(null);
    
    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('audio', audioFile);

      // Call backend API for transcription and analysis
      const response = await fetch('https://truth-weaver.onrender.com/transcribe-and-analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to process audio');
      }

      const result = await response.json();
      
      if (result.success) {
        setTranscript(result.transcript);
        setAnalysis(result.analysis);
      } else {
        throw new Error('Processing failed');
      }
    } catch (error) {
      setError(`Failed to process audio: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-lg p-8 mt-8 mb-4">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-blue-900 mb-2">Truth Weaver</h1>
        <p className="text-blue-700 text-lg">AI-Powered Transcript & Deception Analysis</p>
      </header>
      <main>
        <section className="flex flex-col items-center mb-8">
          <label htmlFor="audio-upload" className="font-semibold mb-2 text-blue-900">Upload Audio File</label>
          <input
            id="audio-upload"
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            className="mb-4"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-gradient-to-r from-blue-400 to-blue-700 text-white rounded-md px-6 py-2 font-semibold transition disabled:bg-blue-200 disabled:cursor-not-allowed mb-2"
          >
            {loading ? 'Processing...' : 'Transcribe & Analyze'}
          </button>
        {error && (
          <div className="text-red-600 mt-1 text-base">
            {error}
            <br />
            <small className="text-red-500">
              Tips: Ensure audio is clear, has speech content, and you have internet connection
            </small>
          </div>
        )}
        </section>

        {transcript && (
          <section className="mb-8 text-left">
            <h2 className="text-xl text-blue-700 font-semibold mb-2">Transcript</h2>
            <pre className="bg-blue-50 rounded-lg p-4 text-base text-gray-800 whitespace-pre-wrap shadow-sm">{transcript}</pre>
          </section>
        )}

        {analysis && (
          <section className="mb-8 text-left">
            <h2 className="text-xl text-blue-700 font-semibold mb-4">AI Analysis</h2>
            <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1 bg-blue-50 rounded-lg p-4 shadow-sm">
                <h3 className="font-semibold text-blue-900 mb-2">Revealed Truth</h3>
                <ul className="list-disc pl-5">
                  {Object.entries(analysis.revealed_truth).map(([key, value]) => (
                    <li key={key} className="mb-1">
                      <span className="font-medium capitalize">{key.replace(/_/g, ' ')}:</span>{' '}
                      {Array.isArray(value) ? value.join(', ') : value}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="flex-1 bg-blue-50 rounded-lg p-4 shadow-sm">
                <h3 className="font-semibold text-blue-900 mb-2">Deception Patterns</h3>
                <ul className="list-disc pl-5">
                  {analysis.deception_patterns.map((pattern, idx) => (
                    <li key={idx} className="mb-2">
                      <span className="font-medium">Type:</span> {pattern.lie_type}
                      <br />
                      <span className="font-medium">Contradictory Claims:</span>
                      <ul className="list-disc pl-5">
                        {pattern.contradictory_claims.map((claim, i) => (
                          <li key={i}>{claim}</li>
                        ))}
                      </ul>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </section>
        )}
      </main>
      <footer className="text-center text-gray-500 text-sm mt-8">
        <p>© {new Date().getFullYear()} Truth Weaver. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
