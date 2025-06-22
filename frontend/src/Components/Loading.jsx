import React from 'react';
import './Loading.css';
import loaderGif from '../assets/Loading.gif'; 

const Loading = () => {
  return (
    <div className="loading-container">
      <img src={loaderGif} alt="Loading..." className="loading-gif" />
    </div>
  );
};

export default Loading;
