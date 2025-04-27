import React from 'react';

interface AnalysisResult {
    match_score: number;
    matched_keywords: string[];
    missing_keywords: string[];
}

interface ResultsDisplayProps {
    result: AnalysisResult;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result }) => {
    return (
        <div style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
            <h2>Analysis Results</h2>
            <p><strong>Match Score:</strong> {result.match_score}%</p>

            <h3>Matched Keywords ({result.matched_keywords.length}):</h3>
            {result.matched_keywords.length > 0 ? (
                <ul>
                    {result.matched_keywords.map((keyword, index) => (
                        <li key={`matched-${index}`}>{keyword}</li>
                    ))}
                </ul>
            ) : (
                <p>No keywords matched.</p>
            )}


            <h3>Missing Keywords ({result.missing_keywords.length}):</h3>
             {result.missing_keywords.length > 0 ? (
                <ul>
                    {result.missing_keywords.map((keyword, index) => (
                        <li key={`missing-${index}`}>{keyword}</li>
                    ))}
                </ul>
             ) : (
                <p>No keywords missing from resume (based on JD).</p>
             )}

            
        </div>
    );
};

export default ResultsDisplay;

export type { AnalysisResult };