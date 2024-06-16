import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ResultItem from './ResultItem';

const Search = () => {
  const [imageString, setImageString] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageLabel, setImageLabel] = useState("")
  const [status, setStatus] = useState('');
  const [isHealthy, setIsHealthy] = useState(false);
  const [healthStatus, setHealthStatus] = useState('Checking health...');

  useEffect(() => {
    // Function to perform health check
    const checkHealth = async () => {
      try {
        const response = await axios.get('http://localhost:8000/health');
        if (response.status === 200 && response.data.status === 'healthy') {
          setIsHealthy(true);
          setHealthStatus('Backend is healthy.');
        } else {
          setHealthStatus('Backend is initializing...');
        }
      } catch (error) {
        setHealthStatus(error.response.data.detail);
      }
    };

    // Perform health check every second until backend is healthy
    const interval = setInterval(() => {
      if (!isHealthy) {
        checkHealth();
      } else {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, [isHealthy]);

  const handleInputChange = (e) => {
    setImageString(e.target.value);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus('Searching image...');

    try {
      // Use the label to search for related images
      const searchResponse = await axios.post('http://localhost:8000/search', { image_data: imageString });
      setImageLabel(searchResponse.data.label)
      // Set the results to be displayed
      setResults(searchResponse.data.image_urls);
      setStatus('Search completed.');
    } catch (error) {
      console.error('Error uploading image or searching:', error);
      setStatus('Error occurred during uploading or searching.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Image Search</h1>
      <p>{healthStatus}</p>
      <form onSubmit={handleSearch}>
        <label>
          Image String:
          <input type="text" value={imageString} onChange={handleInputChange} required />
        </label>

        <p> label: <label>{imageLabel}</label></p>
        <button type="submit" disabled={loading || !isHealthy}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {status && <p>{status}</p>}

      <h2>Results</h2>
      {loading && <p>Loading results...</p>}
      <div className="results-container">
        {results.map((result, index) => (
          <ResultItem key={index} imageUrl={result} />
        ))}
      </div>
    </div>
  );
};

export default Search;
