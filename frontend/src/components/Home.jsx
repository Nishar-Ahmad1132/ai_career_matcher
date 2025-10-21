import React from "react";
import "./Home.css";

const features = [
  {
    title: "AI-Powered Resume Matching",
    desc: "Get your resume analyzed and matched with the best jobs in seconds.",
  },
  {
    title: "Explore Thousands of Jobs",
    desc: "Access thousands of verified job postings with details like skills, company, and location.",
  },
  {
    title: "Smart Match Score",
    desc: "See how well your resume fits each job with our intelligent match scoring system.",
  },
];

const Home = () => {
  return (
    <div className="home-container">
      <section className="hero">
        <div className="hero-content">
          <h1>Find Your Dream Job Faster</h1>
          <p>
            Upload your resume and let AI match you with the best opportunities.
          </p>
          <a href="/resume" className="cta-btn">
            Get Started
          </a>
        </div>
      </section>

      <section className="features">
        {features.map((f, idx) => (
          <div key={idx} className="feature-card">
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
};

export default Home;
