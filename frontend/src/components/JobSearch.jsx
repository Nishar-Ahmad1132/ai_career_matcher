import React, { useState } from "react";
import { searchJobs } from "../api/jobApi";
import "./JobSearch.css";

const JobSearch = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResults([]);
    try {
      const data = await searchJobs(query);
      setResults(data.matches);
    } catch (err) {
      console.error(err);
      alert("Error fetching jobs. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-container">
      <section className="search-hero">
        <h1>Search Your Ideal Job</h1>
        <p>Find jobs that match your skills and preferences instantly.</p>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Enter job title, skills, or location..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </section>

      {results.length > 0 && (
        <section className="results-section">
          <h3>Search Results</h3>
          <div className="results-grid">
            {results.map((job, idx) => (
              <div key={idx} className="result-card">
                <h3>{job.job_title}</h3>
                <p>
                  <strong>Company:</strong> {job.company}
                </p>
                <p>
                  <strong>Location:</strong> {job.location}
                </p>
                <p>
                  <strong>Skills:</strong> {job.skills}
                </p>
                <p>{job.description}</p>
                <a
                  href={job.advertiser_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Job
                </a>
                <p className="match-score">
                  Match Score: {(job.match_score * 100).toFixed(1)}%
                </p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default JobSearch;
