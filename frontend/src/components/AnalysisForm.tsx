import React, { useState, useRef } from 'react';

interface AnalysisFormProps {
    onSubmit: (file: File, jobDescription: string) => void;
    isLoading: boolean;
}

const AnalysisForm: React.FC<AnalysisFormProps> = ({ onSubmit, isLoading }) => {
    const [jobDescription, setJobDescription] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const file = fileInputRef.current?.files?.[0];

        if (file && jobDescription) {
            onSubmit(file, jobDescription);
        } else if (!file) {
            alert('Please select a resume file.');
        } else {
            alert('Please paste the job description.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="resume-file">Upload Resume (.pdf, .docx):</label><br />
                <input
                    type="file"
                    id="resume-file"
                    ref={fileInputRef}
                    accept=".pdf,.docx"
                    required
                    disabled={isLoading}
                />
            </div>
            <div>
                <label htmlFor="job-description">Paste Job Description:</label><br />
                <textarea
                    id="job-description"
                    rows={10}
                    cols={60}
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    required
                    disabled={isLoading}
                />
            </div>
            <button type="submit" disabled={isLoading}>
                {isLoading ? 'Analyzing...' : 'Analyze'}
            </button>
        </form>
    );
};

export default AnalysisForm;