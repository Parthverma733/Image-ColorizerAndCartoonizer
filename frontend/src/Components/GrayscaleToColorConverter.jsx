import React, { useState, useRef } from 'react';
import axios from 'axios';
import './image.css';
import { motion } from 'framer-motion';
const GrayscaleToColorConverter = () => {
    const [originalImage, setOriginalImage] = useState(null);
    const [coloredImage, setColoredImage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setOriginalImage(reader.result);
                setColoredImage(null);
                setError(null);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleConvert = async () => {
        if (!originalImage) {
            setError('Please upload a grayscale image first');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const base64Data = originalImage.split(',')[1];
            const response = await axios.post(
                'http://localhost:8000/colorize', // Backend endpoint
                { image: base64Data },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    responseType: 'json',
                }
            );

            if (response.data && response.data.coloredImage) {
                setColoredImage(`data:image/jpeg;base64,${response.data.coloredImage}`);
            } else {
                setError('Failed to colorize image');
            }
        } catch (err) {
            console.error('Colorization error:', err);
            setError('Error colorizing image. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const triggerFileInput = () => {
        fileInputRef.current.click();
    };

    return (
         <motion.div
            className="home-container"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
        >
        <div className="image">
            <div className="image-converter-container">
                <div className="heading-section">
                     <h1 className="rainbow-text">Grayscale to Colored Converter</h1>
                    <p className="tagline"><strong>Colorize your images with a single click</strong> ✨</p>
                   </div>
                <div className="converter-sections">

                    <div className="upload-section">
                        <h2>Grayscale Image</h2>
                        <div
                            className="upload-area"
                            onClick={triggerFileInput}
                        >
                            {originalImage ? (
                                <img
                                    src={originalImage}
                                    alt="Original"
                                    className="preview-image"
                                />
                            ) : (
                                <div className="upload-prompt">
                                    <p>Click to upload a grayscale image</p>
                                    <p className="small-text">Supports JPG, PNG</p>
                                </div>
                            )}
                        </div>
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleImageUpload}
                            accept="image/*"
                            style={{ display: 'none' }}
                        />
                    </div>

                    <div className="output-section">
                        <h2>Colored Version</h2>
                        <div className="output-area">
                            {coloredImage ? (
                                <img
                                    src={coloredImage}
                                    alt="Colored"
                                    className="preview-image"
                                />
                            ) : (
                                <div className="output-placeholder">
                                    <p>Colorized version will appear here</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="action-section">
                    <button
                        onClick={handleConvert}
                        disabled={!originalImage || isLoading}
                        className="convert-button"
                    >
                        {isLoading ? 'Processing...' : 'Convert to Color'}
                    </button>
                </div>

                {error && <div className="error-message">{error}</div>}
            </div>
        </div>
        </motion.div>
    );
};

export default GrayscaleToColorConverter;
