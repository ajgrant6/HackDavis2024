import './App.css';
import React, { useState } from 'react';
import WalkAbility from './Views/WalkAbility';
import Rights from './Views/Rights';

function App() {
  // State to hold the input value
  const [inputValue, setInputValue] = useState('');

  // States for walk score, transit score, and bike score
  const [walkScore, setWalkScore] = useState(0);
  const [transitScore, setTransitScore] = useState(0);
  const [bikeScore, setBikeScore] = useState(0);

  // Function to handle input changes
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const url = `http://localhost:8080/api/getInfo`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link: inputValue }) // Ensure this matches the key expected by your Flask app
      });
      if (!response.ok) {
        throw new Error(`HTTP status ${response.status}: Network response was not ok`);
      }
      const data = await response.json();
      // Update state with the data from the response
      setWalkScore(data.walkscore);
      setTransitScore(data.transit_score);
      setBikeScore(data.bike_score);
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
        {/* Updated component to use state values */}
        <WalkAbility walkScore={walkScore} transitScore={transitScore} bikeScore={bikeScore} />
        <Rights abortion_access="Legal" lgbt_friendliness="Accepting" />
      </div>
    </div>
  );
}

export default App;
