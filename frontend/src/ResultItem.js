import React from 'react';
import './ResultItem.css';

const ResultItem = ({ imageUrl }) => {

  return (
    <div className="result-item">
      <p>{imageUrl[0]}</p>
      <p> label: {imageUrl[1]} </p>
    </div>
  );
};

export default ResultItem;
