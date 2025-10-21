import React from "react";
import "./ResultCard.css";

const ResultCard = ({ job }) => {
  const skills = job.skills ? job.skills.split(",").map((s) => s.trim()) : [];

  return (
    <div className="result-card">
      <div className="card-header">
        <h3>{job.job_title || "N/A"}</h3>
        <p className="company">{job.company}</p>
      </div>

      <p className="location">
        <strong>Location:</strong> {job.location}
      </p>

      {skills.length > 0 && (
        <div className="skills">
          {skills.map((skill, idx) => (
            <span key={idx} className="skill-badge">
              {skill}
            </span>
          ))}
        </div>
      )}

      <p className="description">{job.description}</p>

      <div className="card-footer">
        <a
          href={job.advertiser_url}
          target="_blank"
          rel="noopener noreferrer"
          className="view-btn"
        >
          View Job
        </a>
        <span className="match-score">
          {(job.match_score * 100).toFixed(1)}%
        </span>
      </div>
    </div>
  );
};

export default ResultCard;
