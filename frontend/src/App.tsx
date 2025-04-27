// src/App.tsx
import React, { useState } from 'react';
import AnalysisForm from './components/AnalysisForm';
import ResultsDisplay, { AnalysisResult } from './components/ResultsDisplay';

const API_URL = 'http://127.0.0.1:8000/analyze/';

function App() {
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async (resumeFile: File, jobDescription: string) => {
        setError(null);
        setAnalysisResult(null);
        setIsLoading(true);

        const formData = new FormData();
        formData.append('resume_file', resumeFile);
        formData.append('job_description', jobDescription);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch (e){

                }
                const errorMsg = errorData?.detail || `API Error: ${response.status} ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data: AnalysisResult = await response.json();
            setAnalysisResult(data);

        } catch (err: any) {
            console.error("Analysis Fetch Error:", err);
            setError(err.message || 'Failed to analyze. Is the backend server running correctly?');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px' }}>
            <h1>AI Resume Analyzer</h1>

            <AnalysisForm onSubmit={handleAnalyze} isLoading={isLoading} />

            {isLoading && <p style={{ marginTop: '15px' }}>Analyzing... Please wait.</p>}

            {error && <p style={{ color: 'red', marginTop: '15px' }}>Error: {error}</p>}

            {analysisResult && !isLoading && <ResultsDisplay result={analysisResult} />}

        </div>
    );
}

export default App;