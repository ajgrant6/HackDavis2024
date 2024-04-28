import './App.css';
import React, { useState } from 'react';
import WalkAbility from './Views/WalkAbility';
import WomansRights from './Views/WomansRights';
import LGBTRights from './Views/LGBTRights';

function App() {
  // State to hold the input value
  const [inputValue, setInputValue] = useState('');
  const [dataFetched, setDataFetched] = useState(false);


  // States for walk score, transit score, and bike score
  const [walkScore, setWalkScore] = useState(0);
  const [transitScore, setTransitScore] = useState(0);
  const [bikeScore, setBikeScore] = useState(0);
  const [walk_description, setWalkDescription] = useState(0);
  const [transit_summary, setTransitSummary] = useState(0);
  const [transit_description, setTransitDescription] = useState(0);
  const [bike_description, setBikeDescription] = useState(0);
  const [ei, setEI] = useState(0);
  const [ei_legal, setEI_Legal] = useState(0);
  const [ei_po, setEI_PO] = useState(0);
  const [genderafirm_legality, setGenderAfirmLegality] = useState(0);
  const [employment_discrimination, setEmploymentDiscrimination] = useState(0);
  const [abortion_policy, setAbortionPolicy] = useState(0);

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
      setEI(data.ei_value);
      setEI_Legal(data.legal_ei_value);
      setEI_PO(data.po_ei_value);
      setWalkDescription(data.walk_description);
      setTransitSummary(data.transit_summary);
      setTransitDescription(data.transit_description);
      setBikeDescription(data.bike_description);
      setGenderAfirmLegality(data.genderafirm_legality);
      setEmploymentDiscrimination(data.employment_discrimination);
      setAbortionPolicy(data.abortion_policy);
      setDataFetched(true);  // Set data fetched to true
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

      {dataFetched && (
        <div className="Features">
          <WalkAbility walkScore={walkScore} transitScore={transitScore} bikeScore={bikeScore} walk_description={walk_description} transit_description={transit_description} transit_summary={transit_summary} bike_description={bike_description}/>
          <WomansRights abortion_policy={abortion_policy} employment_discrimination={employment_discrimination}/>
          <LGBTRights ei={ei} ei_legal={ei_legal} ei_po={ei_po} genderafirm_legality={genderafirm_legality} employment_discrimination={employment_discrimination}/>
        </div>
      )}
    </div>
  );
}

export default App;
