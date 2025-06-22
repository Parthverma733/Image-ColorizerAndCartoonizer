import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Home.css';

const Home = () => {
    return (
        <motion.div
            className="home-container"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
        >
            <div className="hero-section">
                <h1 className="rainbow-text">AI Image <strong>Enhancer</strong></h1>
             
                <p className="tagline"><strong>Cartoonify and Colorize your images with a single click</strong> ✨</p>
               
            </div>

            <div className="about-section">
             <div className="aleft">
                   <h2><em>🚀 What is This?</em></h2>
                <p>
                    This web-based tool uses a combination of <strong>OpenCV, Pillow, and AI models</strong> to let you:
                    <ul>
                        <li>🎨 Cartoonify normal photos with bold edges and smooth shading</li>
                        <li>🌈 Restore color to black-and-white photos using AI colorization</li>
                    </ul>
                </p>
             </div>

             <div className="aright">
                 
             </div>
            </div>

            <div className="how-it-works-section">
              <div className="hleft">
            
              </div>
              <div className="hright">
                  <h2><em>🧠 How It Works</em></h2>
                <ol>
                    <li>Upload an image (JPG or PNG)</li>
                    <li>Click convert — image is sent to the backend</li>
                    <li>AI algorithms process and return the transformed result</li>
                    <li>Preview the result and download it instantly</li>
                </ol>
              </div>
            </div>

            <div className="footer">
                 <div className="hero-buttons">
                    <Link to="/cartoon" className="hero-btn">Cartoon Converter</Link>
                    <Link to="/colorize" className="hero-btn-secondary">Grayscale Colorizer</Link>
                </div>
                <p>Created with ❤️ using React + FastAPI + OpenCV + Pillow</p>
            </div>
        </motion.div>
    );
};

export default Home;
