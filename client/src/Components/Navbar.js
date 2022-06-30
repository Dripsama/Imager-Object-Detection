import React from "react";
import "./Navbar.css";

export default function Navbar() {
  return (
    <div>
      <navbar>
        <h1 className="brand">
          <a style={{ color: "white", textDecoration: "none" }} href="/">
            Imager
          </a>
        </h1>
        <h3 className="about">
          <a href="#about" style={{ color: "white", textDecoration: "none" }}>
            About
          </a>
        </h3>
      </navbar>
    </div>
  );
}
