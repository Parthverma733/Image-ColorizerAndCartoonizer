import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <div className="logo">

                </div>
                <div className="navtitle">
                 Image <strong>Enhancer</strong>
                </div>
            </div>
            <ul className="navbar-links">
                
    <li><Link to="/">Home</Link></li>
                <li>
                    <Link to="/cartoon">Cartoon Converter</Link>
                </li>
                <li>
                    <Link to="/colorize">Grayscale Colorizer</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
