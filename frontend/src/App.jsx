import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Components/Navbar';
import ImageToCartoonConverter from './Components/ImageToCartoonConverter';
import GrayscaleToColorConverter from './Components/GrayscaleToColorConverter';
import Home from './Components/Home';

const App = () => {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/cartoon" element={<ImageToCartoonConverter />} />
                <Route path="/colorize" element={<GrayscaleToColorConverter />} />
            </Routes>
        </Router>
    );
};

export default App;
