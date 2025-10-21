import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">AI Career Matcher</Link>
      </div>
      <div className="navbar-links">
        <Link className={location.pathname === "/" ? "active" : ""} to="/">
          Home
        </Link>
        <Link
          className={location.pathname === "/resume" ? "active" : ""}
          to="/resume"
        >
          Upload Resume
        </Link>
        <Link
          className={location.pathname === "/search" ? "active" : ""}
          to="/search"
        >
          Search Jobs
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
