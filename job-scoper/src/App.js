import './App.css';
import React, { useState } from 'react';
import WalkAbility from './Views/WalkAbility';
import Rights from './Views/Rights';

function App() {
  // State to hold the input value
  const [inputValue, setInputValue] = useState('');

  // State to hold API response data (if needed)
  const [apiResponse, setApiResponse] = useState(null);

  // Function to handle input changes
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  // Function to handle API request
  const handleSearch = async () => {
    try {
      const response = await fetch(`YOUR_API_ENDPOINT?query=${encodeURIComponent(inputValue)}`, {
        method: 'GET', // or 'POST', depending on your API
        headers: {
          'Content-Type': 'application/json',
          // Additional headers
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setApiResponse(data);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };

  return (
    <div className="App">
      <div className='Header'>
        <h1>Job Scoper</h1>
        <p>Find the best city for you to live and work in</p>
        <div className="SearchField">
          <input type="text" size="40" placeholder="Place a LinkedIn or Indeed Job Posting Here"
                 value={inputValue} onChange={handleInputChange} />
          <div className="Spacer"/>
          <button onClick={handleSearch}>Search</button>
        </div>
      </div>

      <div className="Features">
        <WalkAbility walkScore={100} transitScore={100} bikeScore={100} />
        <Rights abortion_access="Legal" lgbt_friendliness="Accepting" />
      </div>
    </div>
  );
}

export default App;
