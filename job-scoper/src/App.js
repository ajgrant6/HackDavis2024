import './App.css';
import React, { useState } from 'react';
import WalkAbility from './Views/WalkAbility';
import WomansRights from './Views/WomansRights';
import LGBTRights from './Views/LGBTRights';
import ResumeHelper from './Views/ResumeHelper';
import MapContainer from './Views/MapContainer';


function App() {
  // State to hold the input value
  const [inputValue, setInputValue] = useState('');
  const [dataFetched, setDataFetched] = useState(false);
  const [loading, setLoading] = useState(false); // State to track loading status

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
  const [lat, setLat] = useState(0);
  const [lon, setLon] = useState(0);

  // Function to handle input changes
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSearch = async () => {
    setLoading(true); // Set loading to true when button is pressed
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
      setLat(data.lat);
      setLon(data.lon);
      console.log(lat)
      console.log(lon)
      setDataFetched(true);  // Set data fetched to true
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setLoading(false); // Set loading to false when data fetching is complete
    }
  };

  return (
    <div className="App">
      <div className='Header'>
        <h1>Job Scoper 🏢🤔</h1>
        <p>Find the best city for you to live and work in</p>
        <div className="SearchField">
          <input type="text" size="40" placeholder="Place a LinkedIn or Indeed Job Posting Here"
                 value={inputValue} onChange={handleInputChange} onKeyPress={(event) => event.key === 'Enter' && handleSearch()} style={{borderRadius: '5px', fontSize: '18px', paddingRight: '5px'}} />
          <div className="Spacer"/>
          <button onClick={handleSearch} style={{borderRadius: '5px', fontSize: '18px', padding: '2px 5px'}}>Search</button>
        </div>
      </div>

      {/* Show loading message while loading */}
      {loading && <img src={require('./loading.gif')} alt="Loading..." />}

      {dataFetched && !loading && (
        <div>
          <div className="Features">
            <WalkAbility walkScore={walkScore} transitScore={transitScore} bikeScore={bikeScore} walk_description={walk_description} transit_description={transit_description} transit_summary={transit_summary} bike_description={bike_description}/>
            <WomansRights abortion_policy={abortion_policy} employment_discrimination={employment_discrimination}/>
            <LGBTRights ei={ei} ei_legal={ei_legal} ei_po={ei_po} genderafirm_legality={genderafirm_legality} employment_discrimination={employment_discrimination}/>
          </div>

          <div style ={{marginTop: '30px', marginBottom: "500px"}}>
          <MapContainer latIn={lat} lonIn={lon} />
          </div>

          <div>
          <ResumeHelper jobLink = {inputValue}/>
          </div>
        </div>
      )}
    </div>
  ); 
}

export default App;
