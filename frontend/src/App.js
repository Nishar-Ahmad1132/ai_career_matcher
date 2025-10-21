import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ResumeUpload from "./components/ResumeUpload";
import Home from "./components/Home";
import JobSearch from "./components/JobSearch";


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/resume" element={<ResumeUpload />} />
        <Route path="/search" element={<JobSearch />} />
      </Routes>
    </Router>
  );
}

export default App;
