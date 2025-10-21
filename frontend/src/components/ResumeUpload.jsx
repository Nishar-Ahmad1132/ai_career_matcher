import React, { useState } from "react";
import { matchResume } from "../api/resumeApi";
import ResultCard from "./ResultCard";
import "./ResumeUpload.css";

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!validTypes.includes(selectedFile.type)) {
      alert("Unsupported file type. Please upload PDF or DOCX.");
      return;
    }

    setFile(selectedFile);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setResults([]);
    try {
      const data = await matchResume(file);
      setResults(data.matches);
    } catch (err) {
      console.error(err);
      alert("Error matching resume. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-upload-container">
      <h2>Upload Your Resume</h2>

      <div className="upload-form">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="file-input"
        />
        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          className="upload-btn"
        >
          {loading ? <div className="loader"></div> : "Match Resume"}
        </button>
      </div>

      {results.length > 0 && (
        <div className="results-section">
          <h3>Top Job Matches</h3>
          <div className="results-grid">
            {results.map((job, idx) => (
              <ResultCard key={idx} job={job} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
