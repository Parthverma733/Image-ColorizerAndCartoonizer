

import React, { useState, useRef } from 'react';
import axios from 'axios';
import './image.css';
import { motion } from 'framer-motion';
import Loading from './Loading';

const ImageToCartoonConverter = () => {
    const [originalImage, setOriginalImage] = useState(null);
    const [cartoonImage, setCartoonImage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    const resizeImage = (base64Str, maxSize = 512) => {
        return new Promise((resolve) => {
            const img = new Image();
            img.src = base64Str;
            img.onload = () => {
                let width = img.width;
                let height = img.height;

                if (width > height && width > maxSize) {
                    height *= maxSize / width;
                    width = maxSize;
                } else if (height > maxSize) {
                    width *= maxSize / height;
                    height = maxSize;
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                resolve(canvas.toDataURL('image/jpeg'));
            };
        });
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setOriginalImage(reader.result);
                setCartoonImage(null);
                setError(null);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleConvert = async () => {
        if (!originalImage) {
            setError('Please upload an image first');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const resized = await resizeImage(originalImage);
            const base64Data = resized.split(',')[1];

            const response = await axios.post(
                'http://localhost:8000/cartoonize',
                { image: base64Data },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    responseType: 'json',
                }
            );

            if (response.data && response.data.cartoonImage) {
                setCartoonImage(`data:image/jpeg;base64,${response.data.cartoonImage}`);
            } else {
                setError('Failed to process image');
            }
        } catch (err) {
            console.error('Conversion error:', err);
            setError('Error converting image. Please try again.');
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
                        <h1 className="rainbow-text">Image to Cartoon Converter</h1>
                        <p className="tagline"><strong>Cartoonify your images with a single click</strong> ✨</p>
                    </div>

                    <div className="converter-sections">
                        <div className="upload-section">
                            <h2>Original Image</h2>
                            <div className="upload-area" onClick={triggerFileInput}>
                                {originalImage ? (
                                    <img src={originalImage} alt="Original" className="preview-image" />
                                ) : (
                                    <div className="upload-prompt">
                                        <p>Click to upload an image</p>
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
                            <h2>Cartoon Version</h2>
                            <div className="output-area">
                                {cartoonImage ? (
                                    <img src={cartoonImage} alt="Cartoon" className="preview-image" />
                                ) : (
                                    <div className="output-placeholder">
                                        {isLoading ? <Loading /> : <p>Cartoon version will appear here</p>}
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
                            {isLoading ? 'Processing...' : 'Convert to Cartoon'}
                        </button>
                    </div>

                    {error && <div className="error-message">{error}</div>}
                </div>
            </div>
        </motion.div>
    );
};

export default ImageToCartoonConverter;
